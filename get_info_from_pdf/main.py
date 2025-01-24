import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.llms import Ollama
from dotenv import load_dotenv
import os

load_dotenv()

def get_pdf_txt(pdf_f):
    text = ""
    for pdf in pdf_f:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_txt_chunks(txt):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(txt)
    return chunks

def get_vector_store(txt_chunks):
    ollama_emb = OllamaEmbeddings(model="llama3.2")
    vector_store = FAISS.from_texts(txt_chunks, embedding=ollama_emb)
    vector_store.save_local("faiss_store")

def get_chat_chain(db):
    prompt_template = """
    "system" Answer the question as detailed as possible from the provided context, make sure to provide context just say,
    "answer is not available in the context", don't provide the wrong answer.\n\n
    context:\n{context}\n
    question: \n{input}\n

    answer:
    """
    llm = Ollama(model="llama3.2")
    prompt = ChatPromptTemplate.from_template(template=prompt_template, input_variable=["context", "question"])
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = db.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    print(f"Retrieval chain: {type(retrieval_chain)}")
    return retrieval_chain

def rag_model(query, retrieval_chain):
    print(f"Retrieval chain in rag fn: {type(retrieval_chain)}")  # Debugging line
    res = retrieval_chain.invoke({"input": query})
    print(f"Response: {res}")  # Debugging line
    if isinstance(res, dict) and 'answer' in res:
        answer = res['answer']
    else:
        answer = "Sorry, I couldn't find an answer to your question."
    return answer

# Streamlit UI
def main():
    st.title("PDF Query Application")
    
    # Upload PDF files
    uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        # Process the PDFs
        st.write("Processing your PDFs...")
        pdf_text = get_pdf_txt(uploaded_files)
        text_chunks = get_txt_chunks(pdf_text)
        get_vector_store(text_chunks)  # Create vector store

        st.success("PDFs processed successfully! You can now ask questions.")

        # Ask a question based on the content of the PDFs
        user_query = st.text_input("Ask a question based on the PDF content:")

        if user_query:
            st.write("Searching for the answer...")

            ollama_emb = OllamaEmbeddings(model="llama3.2")
            new_db = FAISS.load_local("faiss_store", ollama_emb, allow_dangerous_deserialization=True)
            # docs = new_db.similarity_search(user_query)
            
            # Now, get the retrieval chain
            retrieval_chain = get_chat_chain(new_db)

            # Pass documents and query to rag_model
            response = rag_model(user_query, retrieval_chain)
            st.write(f"Answer: {response}")
    
if __name__ == "__main__":
    main()
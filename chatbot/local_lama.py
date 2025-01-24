from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama 

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANHCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

## Prompt Template
prompt = ChatPromptTemplate([
    ("system", "You're a helpful assistant. Please response to the user quries"),
    ("user", "Question: {question}")
])

## Streamlit framework
st.title("Langchain demo with LLAma API")
input_text = st.text_input("Search the topic you want")

## Ollama LLAma3.2
llm = Ollama(model="llama3.2")
output_parser = StrOutputParser()
chain = prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({"question": input_text}))
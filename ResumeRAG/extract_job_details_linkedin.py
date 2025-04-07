import requests
from bs4 import BeautifulSoup

def extract_job_details(url):
    """
    Extracts job details from the given LinkedIn job search URL.

    Args:
        url: The URL of the LinkedIn job search results page.

    Returns:
        A list of dictionaries, where each dictionary represents a job
        and contains the job title, company name, location, date of post,
        and company link (href).
    """

    html_file = requests.get(url)
    soup = BeautifulSoup(html_file.text, 'lxml')

    jobs_data = []
    jobs = soup.find_all('div', class_='base-search-card__info')
    for job in jobs:
        job_title = job.find('h3', class_='base-search-card__title').text.strip()
        company_name = job.find('h4', class_='base-search-card__subtitle').text.strip()
        
        # Extract href of anchor tag
        company_link_element = job.find('h4', class_='base-search-card__subtitle').find('a')
        company_link = company_link_element['href'] if company_link_element else "N/A"
        
        location = job.find('span', class_='job-search-card__location').text.strip()
        
        # Check if the date_of_post element exists before accessing its text
        date_of_post_element = job.find('time', class_='job-search-card__listdate')
        date_of_post = date_of_post_element.text.strip() if date_of_post_element else "N/A"

        jobs_data.append({
            'Job Title': job_title,
            'Company Name': company_name,
            'Location': location,
            'Date of Post': date_of_post,
            'Company Link': company_link
        })

    return jobs_data
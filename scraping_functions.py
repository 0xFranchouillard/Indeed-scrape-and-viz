import requests
from bs4 import BeautifulSoup
import time
import json
from config import headers,URLJob

def make_soup(URL):
    print(URL)

    try:
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        print("Erreur à la connexion...\nErreur HTTP :", response.status_code)
        if((requests.get('https://google.fr')).status_code != 200):
            print("Problème de connexion Internet...")
            exit(1)
    return soup

def extract_data_from_jobs_pages(job, div):
    job['jobName'] = div.find(name='a', attrs={'data-tn-element': 'jobTitle'})['title']

    job['companyName'] = div.find(name='span', attrs={'class': 'company'}).text.strip()

    job['cityName'] = div.find(name='span', attrs={'class': 'location accessible-contrast-color-location'}).text.strip()

    job['jobShortDescription'] = div.find('div', attrs={'class': 'summary'}).text.strip()

    job['rating'] = div.find(name='span', attrs={'class': 'ratingsContent'}).text.strip()

    job['jobLink'] = div['data-jk']

    try:
        soup = make_soup(URLJob + job['jobLink'])
        job['jobDataFromLink'] = get_job_data_from_job_soup(soup=soup)
        time.sleep(2)
    except:
        pass
    return job

def extract_data_from_job_page(job, div):
    job['jobType'] = div.find(name='span', attrs={'class': 'jobsearch-JobMetadataHeader-item icl-u-xs-mt--xs'}).text.strip()
    job['jobSalary'] = div.find(name='span', attrs={'class': 'icl-u-xs-mr--xs'}).text.strip()
    return job

def get_job_data_from_job_soup(soup):
    job_data = dict()
    job = extract_data_from_job_page(job_data, soup.find(name='div', attrs={'class': 'jobsearch-JobMetadataHeader-item'}))
    return json.dumps(job)

def get_jobs_pages_from_page_soup(jobs, soup):
    """for div in soup.find_all(name='div', attrs={'class': 'row'}):
        job = dict()
        job = extract_data_from_jobs_pages(job, div)
        jobs.append(job)"""
    div = soup.find(name='div', attrs={'class': 'row'})
    job = dict()
    job = extract_data_from_jobs_pages(job, div)
    jobs.append(job)
    return jobs

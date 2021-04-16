import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import pprint
from pymongo import MongoClient
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
    for jobName in div.find_all(name='a', attrs={'data-tn-element': 'jobTitle'}):
        job['jobName'] = jobName['title']

    for companyName in div.find_all(name='span', attrs={'class': 'company'}):
        job['companyName'] = companyName.text.strip()

    for cityName in div.findAll(name='span', attrs={'class': 'location accessible-contrast-color-location'}):
        job['cityName'] = cityName.text.strip()

    for jobShortDescription in div.findAll('div', attrs={'class': 'summary'}):
        job['jobShortDescription'] = jobShortDescription.text.strip()

    for jobRating in div.findAll(name='span', attrs={'class': 'ratingsContent'}):
        job['rating'] = jobRating.text.strip()

    job['jobLink'] = div['data-jk']

    try:
        soup = make_soup(URLJob + job['jobLink'])
        job['jobDataFromLink'] = get_job_data_from_job_soup(soup=soup)
        time.sleep(2)
    except:
        pass
    return job

def extract_data_from_job_page(job, div):
    for jobType in div.findAll(name='span', attrs={'class': 'jobsearch-JobMetadataHeader-item icl-u-xs-mt--xs'}):
        jobTypes = jobType.text.strip().strip('-  ').split(',')
        jobTypesSplit = []
        for type in jobTypes:
            jobTypesSplit.append(type.lstrip())
    for jobSalary in div.findAll(name='span', attrs={'class': 'icl-u-xs-mr--xs'}):
        job['jobSalary'] = jobSalary.text.strip()
    return job

def get_job_data_from_job_soup(soup):
    for div in soup.find_all(name='div', attrs={'class': 'jobsearch-JobMetadataHeader-item'}):
        job_data = dict()
        job = extract_data_from_job_page(job_data, div)
    return json.dumps(job)

def get_jobs_pages_from_page_soup(jobs, soup):
    for div in soup.find_all(name='div', attrs={'class': 'row'}):
        job = dict()
        job = extract_data_from_jobs_pages(job, div)
        jobs.append(job)
    return jobs

import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import pprint


def extract_data_from_result(soup):
    jobsNames = []
    jobsShortDescriptions = []
    companiesNames = []
    citiesNames = []
    for div in soup.find_all(name='div', attrs={'class': 'row'}):

        for jobName in div.find_all(name='a', attrs={'data-tn-element': 'jobTitle'}):
            jobsNames.append(jobName['title'])

        for companyName in div.find_all(name='span', attrs={'class': 'company'}):
            companiesNames.append(companyName.text.strip())

    for cityName in soup.findAll('span', attrs={'class': 'location accessible-contrast-color-location'}):
        citiesNames.append(cityName.text)

    for jobShortDescription in soup.findAll('div', attrs={'class': 'summary'}):
        jobsShortDescriptions.append(jobShortDescription.text.strip())

    return jobsNames, jobsShortDescriptions, companiesNames, citiesNames


def extract_data_from_jobs_pages(job, div):
    for jobName in div.find_all(name='a', attrs={'data-tn-element': 'jobTitle'}):
        job['jobsNames'] = (jobName['title'])

    for companyName in div.find_all(name='span', attrs={'class': 'company'}):
        job['companiesNames'] = (companyName.text.strip())

    for cityName in div.findAll(name='span', attrs={'class': 'location accessible-contrast-color-location'}):
        job['citiesNames'] = (cityName.text.strip())

    for jobShortDescription in div.findAll('div', attrs={'class': 'summary'}):
        job['jobsShortDescriptions'] = (jobShortDescription.text.strip())

    return job


def get_jobs_pages_from_result(jobs, soup):
    for div in soup.find_all(name='div', attrs={'class': 'row'}):
        job = dict()
        job = extract_data_from_jobs_pages(job, div)
        jobs.append(job)
    return jobs


if __name__ == '__main__':
    URL = 'https://www.indeed.fr/jobs?q=data+analyst&l=Lyon&start=10'
    response = requests.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        print("Erreur à la connexion...\nErreur HTTP :", response.status_code)

    extract_data_from_result(soup)
    data = get_jobs_pages_from_result(jobs = [],soup = soup)
    columns = ['id','jobsNames', 'companiesNames', 'citiesNames', 'jobsShortDescriptions']

    with open('data.json', 'w') as fp:
        json.dump(data, fp, sort_keys=True, indent=2, ensure_ascii=False)

    df = pd.read_json('data.json')
    df.to_csv('data.csv')
import json
import re
import time

import requests
from bs4 import BeautifulSoup


def make_soup(URL):
    print(URL)
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7 (compatible; Googlebot-Mobile/2.1; +http://www.google.com/bot.html)'}
    try:
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
    except:
        print("Erreur à la connexion...\nErreur HTTP :", response.status_code)
        if((requests.get('https://google.fr')).status_code != 200):
            print("Problème de connexion Internet...")
            exit(1)
    return soup

def extract_data_from_jobs_pages(job, div):
    print("ICI")

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
        print("ICI")
        pass
    return job


def extract_data_from_job_page(job, div):
    for jobType in div.findAll(name='span', attrs={'class': 'jobsearch-JobMetadataHeader-item icl-u-xs-mt--xs'}):
        job['jobType'] = jobType.text.strip()
    for jobSalary in div.findAll(name='span', attrs={'class': 'icl-u-xs-mr--xs'}):
        print("->" + jobSalary)
        job['jobSalary'] = jobSalary.text.strip()
        print("salary : " + job['jobSalary'])
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

if __name__ == '__main__':
    """soup = make_soup('http://api.scraperapi.com?api_key=fb6c7af53a0027b0d89358290018eed7&url=https://www.indeed.fr/voir-emploi?jk=2d7e513fec05f54d')
    regex = re.compile(r'Salary:[^<!:\\]+', flags=re.M)
    l = re.findall(regex, soup.text)
    print(l)"""
    #data = get_jobs_pages_from_page_soup(jobs=[], soup=soup)

    #<div class="jobsearch-JobMetadataHeader-item">
    #<span class="jobsearch-JobMetadataHeader-item icl-u-xs-mt--xs">CDI
import re

import requests
from bs4 import BeautifulSoup
import time
import json
from config import headers, URLJob
from mongodb_create_n_read import import_to_mongo
from config import URL


def make_soup(URL):
    print(URL)

    try:
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        print("Erreur à la connexion...\nErreur HTTP :", response.status_code)
        if ((requests.get('https://google.fr')).status_code != 200):
            print("Problème de connexion Internet...")
            exit(1)
    return soup


def extract_data_from_jobs_pages(job, div):
    job['jobName'] = div.find(name='a', attrs={'data-tn-element': 'jobTitle'})['title']

    job['companyName'] = div.find(name='span', attrs={'class': 'company'}).text.strip()

    job['cityName'] = div.find(name='span', attrs={'class': 'location accessible-contrast-color-location'}).text.strip()

    job['jobShortDescription'] = div.find('div', attrs={'class': 'summary'}).text.strip()

    job['rating'] = float(div.find(name='span', attrs={'class': 'ratingsContent'}).text.strip().replace(',','.'))

    job['jobLink'] = div['data-jk']

    try:
        soup = make_soup(URLJob + job['jobLink'])
        job['jobDataFromLink'] = get_job_data_from_job_soup(soup=soup)
        time.sleep(2)
    except:
        pass
    return job


def extract_data_from_job_page(job, div):
    try:
        job['jobType'] = div.find(name='span',attrs={'class':'jobsearch-JobMetadataHeader-item icl-u-xs-mt--xs'}).text.strip()
    except:
        job['jobType'] = "UNKNOW"
    try:
        job['jobSalary'] = div.find(name='span', attrs={'class': 'icl-u-xs-mr--xs'}).text.strip()
    except:
        job['jobSalary']= "UNKNOW"

    return job


def extract_niv_etude(job, soup):
    for p in soup.find_all(name='p'):
        try:
            if(re.findall('Bac.*[^</p>]',p.text)):
                for level in re.findall('Bac.*[^</p>]',p.text):
                    job['Level_study'] = level
        except:
            pass
    return job

def get_job_data_from_job_soup(soup):
    job_data = dict()
    job = extract_data_from_job_page(job_data,
                                     soup.find(name='div', attrs={'class': 'jobsearch-JobMetadataHeader-item'}))
    try:
        job = extract_niv_etude(job, soup.find('div', attrs={'class' : 'jobsearch-jobDescriptionText'}))
    except:
        pass

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


def form_to_scrap_to_mongo(jobName, cityName, companyName):
    number_pages_to_scrape = 1
    for i in range(0, number_pages_to_scrape):
        soup = make_soup(URL + jobName + "&l=" + cityName + "&start=" + str(i * 10) + "&rbc=" + companyName + "&radius=0")
        data = get_jobs_pages_from_page_soup(jobs=[], soup=soup)

        with open('data.json', 'w') as fp:
            json.dump(data, fp, sort_keys=True, indent=2, ensure_ascii=False)

        import_to_mongo(data)

import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import pprint
from pymongo import MongoClient

""""
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
"""


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
        job['jobType'] = jobType.text.strip()
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


def import_to_mongo(data):
    client = MongoClient("mongodb://localhost:27017")
    db = client.indeed_db
    collection = db.indeed_collection

    for i in data:
        try:
            collection.insert_one(i)
            print("Une offre de chez", i['companyName'], "en tant que ", i['jobName']," à bien été ajoutée à la base !")
        except:
            print("Duplicité de l'offre ", i['jobName'])

def make_soup(URL):
    print(URL)
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7 (compatible; Googlebot-Mobile/2.1; +http://www.google.com/bot.html)'}
    try:
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        print("Erreur à la connexion...\nErreur HTTP :", response.status_code)
        if((requests.get('https://google.fr')).status_code != 200):
            print("Problème de connexion Internet...")
            exit(1)
    return soup


if __name__ == '__main__':
    URL = 'http://api.scraperapi.com?api_key=fb6c7af53a0027b0d89358290018eed7&url=https://www.indeed.fr/jobs?q='
    URLJob = 'http://api.scraperapi.com?api_key=fb6c7af53a0027b0d89358290018eed7&url=https://www.indeed.fr/voir-emploi?jk='
    # cities = ['Paris','Lyon','Bordeaux','Asnières sur Seine']
    # jobs_list = ['Data Analyst','Data Scientist','Data engineer','ML engineer']
    cities = ['Saint-Paul-Trois-Châteaux (26)']
    jobs_list = ['agent de nettoyage chimique fabrication industriel chef d Equipe']
    number_pages_to_scrape = 1

    for city in cities:
        city = '+'.join(city.split(' '))
        for job in jobs_list:
            job = '+'.join(job.split(' '))
            for i in range(0, number_pages_to_scrape): #tester si il y a assez d'offres
                soup = make_soup(URL + job + "&l=" + city + "&start=" + str(i * 10))
                data = get_jobs_pages_from_page_soup(jobs=[], soup=soup)

                with open('data.json', 'w') as fp:
                    json.dump(data, fp, sort_keys=True, indent=2, ensure_ascii=False)

                import_to_mongo(data)

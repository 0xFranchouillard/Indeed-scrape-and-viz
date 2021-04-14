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
    job['jobLink'] = div['data-jk']
    for jobName in div.find_all(name='a', attrs={'data-tn-element': 'jobTitle'}):
        job['jobName'] = (jobName['title'])

    for companyName in div.find_all(name='span', attrs={'class': 'company'}):
        job['companyName'] = (companyName.text.strip())

    for cityName in div.findAll(name='span', attrs={'class': 'location accessible-contrast-color-location'}):
        job['cityName'] = (cityName.text.strip())

    for jobShortDescription in div.findAll('div', attrs={'class': 'summary'}):
        job['jobShortDescription'] = (jobShortDescription.text.strip())
    return job


def get_jobs_pages_from_result(jobs, soup):
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
            print("Une offre de chez",i['companyName'],"en tant que ",i['jobName']," à bien été ajoutée à la base !")
        except:
            print("Duplicité de l'offre ", i['jobName'])


def make_soup(URL):
    headers = {'User-Agent':'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7 (compatible; Googlebot-Mobile/2.1; +http://www.google.com/bot.html)'}
    response = requests.get(URL,headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        print("Erreur à la connexion...\nErreur HTTP :", response.status_code)
        exit(code=1)
    return soup


if __name__ == '__main__':
    URL = 'http://api.scraperapi.com?api_key=fb6c7af53a0027b0d89358290018eed7&url=https://www.indeed.fr/jobs?q='

    #cities = ['Paris','Lyon','Bordeaux','Asnières sur Seine']
    #jobs_list = ['Data Analyst','Data Scientist','Data engineer','ML engineer']
    cities = ['Lyon']
    jobs_list = ['Vendeur']
    number_pages_to_scrape = 1

    for city in cities:
        city = '+'.join(city.split(' '))
        for job in jobs_list:
            job = '+'.join(job.split(' '))
            for i in range(0, number_pages_to_scrape):
                soup = make_soup(URL + job + "&l=" + city + "&start=" + str(i * 10))
                # extract_data_from_result(soup)
                data = get_jobs_pages_from_result(jobs=[], soup = soup)
                #columns = ['jobsNames', 'companiesNames', 'citiesNames', 'jobsShortDescriptions']

                with open('data.json', 'w') as fp:
                    json.dump(data, fp, sort_keys=True, indent=2, ensure_ascii=False)

                import_to_mongo(data)
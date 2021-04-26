from scraping_functions import *
from mongodb_create_n_read import *
from config import URL
from flaskApp import app

if __name__ == '__main__':
    # cities = ['Paris','Lyon','Bordeaux','Asnières sur Seine']
    # jobs_list = ['Data Analyst','Data Scientist','Data engineer','ML engineer']

    # cities = ['La Défense']
    # jobs_list = ['Data Analyst']
    # number_pages_to_scrape = 1
    #
    # for city in cities:
    #     city = '+'.join(city.split(' '))
    #     for job in jobs_list:
    #         job = '+'.join(job.split(' '))
    #         for i in range(0, number_pages_to_scrape): #tester si il y a assez d'offres
    #             soup = make_soup(URL + job + "&l=" + city + "&start=" + str(i * 10) + "&radius=0")
    #             data = get_jobs_pages_from_page_soup(jobs=[], soup=soup)
    #
    #             with open('data.json', 'w') as fp:
    #                 json.dump(data, fp, sort_keys=True, indent=2, ensure_ascii=False)
    #
    #             import_to_mongo(data)
    app.run(debug=True)


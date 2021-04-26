from pymongo import MongoClient
from config import URLmongo
from bson.json_util import dumps


def import_to_mongo(data):
    client = MongoClient(URLmongo)
    db = client.indeed_db
    collection = db.indeed_collection
    try:
        db.indeed_collection.create_index('jobLink', unique=True)
    except:
        pass

    for i in data:
        try:
            collection.insert_one(i)
            print("Une offre de chez", i['companyName'], "en tant que", i['jobName'],
                  "à bien été ajoutée à la base !")
        except:
            print("Duplicité de l'offre ", i['jobName'])


def export_to_mongo():
    client = MongoClient(URLmongo)
    db = client.indeed_db
    collection = db.indeed_collection

    data = collection.find()
    return list(data)


def export_to_mongo_research(jobName, city, companyName):
    client = MongoClient(URLmongo)
    db = client.indeed_db
    collection = db.indeed_collection

    data = collection.find({"jobName": {'$regex': jobName, '$options': 'si'}, "cityName": {'$regex': city, '$options': 'si'}, "companyName": {'$regex': companyName, '$options': 'si'}})
    return list(data)

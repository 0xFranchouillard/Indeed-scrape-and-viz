from pymongo import MongoClient
from config import URLmongo
from bson.json_util import dumps


def import_to_mongo(data):
    client = MongoClient(URLmongo)
    db = client.indeed_db
    collection = db.indeed_collection
    db.indeed_collection.create_index('jobLink', unique=True)

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

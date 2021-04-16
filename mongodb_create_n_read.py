from pymongo import MongoClient
from config import URLmongo

def import_to_mongo(data):
    client = MongoClient(URLmongo)
    db = client.indeed_db
    collection = db.indeed_collection

    for i in data:
        try:
            collection.insert_one(i)
            print("Une offre de chez", i['companyName'], "en tant que ", i['jobName']," à bien été ajoutée à la base !")
        except:
            print("Duplicité de l'offre ", i['jobName'])

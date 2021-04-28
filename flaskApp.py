import pandas as pd
from flask import Flask, render_template
from matplotlib import pyplot as plt
from mongodb_create_n_read import *
from formsFlask import *
from scraping_functions import form_to_scrap_to_mongo
import seaborn as sns

app = Flask(__name__)

app.config['SECRET_KEY'] = '56ef8b97b9a841c8d8977223787a1016'

@app.route('/', methods=['GET', 'POST'])
def home():
    graphNote()
    graphScore()
    graphHiring()
    return render_template("GraphIndeed.html")


@app.route('/search', methods=['GET', 'POST'])
def search():
    posts = export_to_mongo()
    form = ResearchForm()
    if form.validate_on_submit():
        """scrap_thread = threading.Thread(target=form_to_scrap_to_mongo,args=(form.jobName.data, form.city.data, form.companyName.data))
        scrap_thread.start()"""
        posts = export_to_mongo_research(form.jobName.data, form.city.data, form.companyName.data)
        if len(posts) < 5:
            form_to_scrap_to_mongo(form.jobName.data, form.city.data, form.companyName.data)
        posts = export_to_mongo_research(form.jobName.data, form.city.data, form.companyName.data)
        return render_template("ScrapeIndeed.html", posts=posts, len=len(posts), form=form)

    return render_template("ScrapeIndeed.html", posts=posts, len=len(posts), form=form)

def graphNote():
    client = MongoClient(URLmongo)
    db = client.indeed_db
    collection = db.indeed_collection
    cur = collection.aggregate(
        [{"$group": {"_id": "$cityName", "showsNumber": {"$sum": 1}}}, {'$sort': {'showsNumber': -1}}, {'$limit': 5}])
    df = pd.DataFrame(list(cur))
    plt.title('Le nombre de postes en fonction de la ville')
    sns.barplot(x='_id', y='showsNumber', data=df)
    plt.savefig("static/job_per_note.png")

def graphScore():
    client = MongoClient(URLmongo)
    db = client.indeed_db
    collection = db.indeed_collection
    cur = collection.aggregate([{"$group":
                                     {"_id": "$companyName",
                                      "avgRating":
                                          {"$avg": '$rating'}
                                      }},
                                {'$sort': {'avgRating': -1}},
                                {'$limit': 5}])
    df = pd.DataFrame(list(cur))
    plt.title('Les 5 sociétés ayant le meilleur score')
    sns.barplot(x='_id', y='avgRating', data=df)
    plt.savefig("static/top_five_company.png")

def graphHiring():
    client = MongoClient(URLmongo)
    db = client.indeed_db
    collection = db.indeed_collection
    cur = collection.aggregate([{"$group":
                                     {"_id": "$companyName",
                                      "jobSum":
                                          {"$sum": 1}
                                      }},
                                {'$sort': {'jobSum': -1}},
                                {'$limit': 5}])

    df_res = pd.DataFrame(list(cur))
    colors = ['#f7a889', '#be7c89']
    df_res.pivot_table('_id', index='_id', aggfunc='sum').plot(kind='pie', subplots=True, autopct='%1.1f%%',
                                                               shadow=True, figsize=(8, 8), startangle=90)
    plt.legend(loc='upper right')
    plt.title('Les 5 entreprises qui recrutent le plus')
    plt.savefig("static/top_five_hiring_company.png")
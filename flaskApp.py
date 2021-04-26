from flask import Flask, render_template
from mongodb_create_n_read import *
from formsFlask import ResearchForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '56ef8b97b9a841c8d8977223787a1016'


@app.route('/', methods=['GET', 'POST'])
def home():
    posts = export_to_mongo()
    form = ResearchForm()
    if form.validate_on_submit():
        # print("jobName : "+form.jobName.data)
        # print("city : "+form.city.data)
        # print("companyName : "+form.companyName.data)
        # print(export_to_mongo_research(form.jobName.data, form.city.data, form.companyName.data))
        posts = export_to_mongo_research(form.jobName.data, form.city.data, form.companyName.data)
        return render_template("ScrapeIndeed.html", posts=posts, len=len(posts), form=form)
    return render_template("ScrapeIndeed.html", posts=posts, len=len(posts), form=form)

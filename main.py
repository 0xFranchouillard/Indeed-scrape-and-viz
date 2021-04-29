from scraping_functions import *
from mongodb_create_n_read import *
from config import URL
from flaskApp import app

if __name__ == '__main__':
    app.run(debug=True)

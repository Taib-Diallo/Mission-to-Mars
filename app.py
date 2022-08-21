from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
# import flask_pymongo
import scrape_mars
import sys
from json import dumps

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/scraped_data'
mongo = PyMongo(app)

@app.route('/')
def home():
    scraped_data = list(mongo.db.mars_info.find())[-1]
    print(scraped_data)
    del scraped_data['_id']
    # return (scraped_data)
    print(scraped_data)
    
    return render_template("index.html", mars = scraped_data)

@app.route('/scrape')
def scrape():
    # print(PyMongo.__version__)
      # create a listings database
    mars_info = mongo.db.mars_info

    mars_scraped = scrape_mars.scrape()
    mars_info.insert_one(mars_scraped)
    
    # return a message to our page so we know it was successful.
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
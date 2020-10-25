
from flask import Flask, render_template
from flask_pymongo import PyMongo

import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def Index():
    mars=  mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape/")
def Scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.All_Scrape()
    mars.update({},mars_data,Upsert = True)
    return "Here's that scrape you requested"

if __name__ == "__main__":
    app.run(debug="True")




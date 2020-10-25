from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import time
import re


def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromdriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "hemispheres": hemisphers(browser),
        "weather": twitter_weather(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

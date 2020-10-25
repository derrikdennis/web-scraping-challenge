

#Setting up our packages
from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd

#Using the Splinter Package to go into the websites we'll need for scraping
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=True)


#Scraping the latest news from NASA's Mars website.

def NASA_mars_news(browser):
    url = "https://mars.nasa.gov/news"
    browser.visit(url)

    #letting the JavaScript components load
    time.sleep(5)

    #Use Beautiful Soup to read in HTML code
    soup = BeautifulSoup(browser.html, "html.parser")

    #The news links are in a section 'UL' section with a class of 'item_list'
    section = soup.find('ul',attrs={"class":"item_list"})

    #Capturing the news aritcles on the page.

    news = section.find_all("li",attrs={"class":"slide"})
    newsDate = []
    newsHeader = []
    newsInfo = []
    for new in news:
        items = new.find("div", attrs={"class":"list_text"})
        itemDate = items.find("div",attrs={"class":"list_date"}).string
        itemHeader = items.find("div",attrs={"class":"content_title"}).string
        itemBody = items.find("div",attrs={"class":"article_teaser_body"}).string
        newsDate.append(itemDate)
        newsHeader.append(itemHeader)
        newsInfo.append(itemBody)

    #Getting the latest headline.
    news_date = newsDate[0]
    news_title = newsHeader[0]
    news_p = newsInfo[0]
    return news_date, news_title, news_p


# Capture the Featured Image on the JPL Mars Space Images Page

def jpl_image(browser):

    #Setting up the Url in two parts so we can use base url later to attach the image.

    jpl_base_url = "https://www.jpl.nasa.gov"
    jpl_search_url = "/spaceimages/?search=&category=Mars"


    #Opening the website.
    browser.visit(jpl_base_url + jpl_search_url)


    #Clicking on the button to get to the feature image.

    targetID =  'full_image'
    browser.find_by_id(targetID).click()


    #Clicking on the "more info" button to get capture the largest possible image.
    browser.click_link_by_partial_text("more info")


    #Using BeautifulSoup to look at the HTML data
    imagesoup = BeautifulSoup(browser.html, "html.parser")


    #Capturing the URL of the featured image.
    imageLocation = imagesoup.find('figure',attrs={"class":"lede"}).find("a")
    image_url = (imageLocation.get('href'))
    featured_image_url = (jpl_base_url + image_url)
    return featured_image_url


# Capturing the latest weather from Mars using Twitter

def Wx_Mars(browser):

    #Visiting the Twitter website for the latest weather from Mars
    mars_WX = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_WX)

    #Giving Twitter a little time to load JavaScript components
    time.sleep(5)

    #Creating the soup to look at the HTML Code 
    WX_soup = BeautifulSoup(browser.html, "html.parser")


    #Capturing the latest weather data from InSign Space rocket which touched down on May 5, 2018. 

    tweets = WX_soup.find_all("span", attrs={"class":{"css-901oao","r-qvutc0"}})
    mars_WX_Reports = []
    for tweet in tweets:
        tweet_text = tweet.text
        tt = tweet_text.replace("\n"," ").replace("º","")

        if " sol " in tt:
            mars_WX_Reports.append(tt)

    Mars_WX = mars_WX_Reports[0]
    return Mars_WX


# Create a table through Pandas read_HTML process to capture facts about Mars.


def Mars_Facts():
    #Visiting the website through Pandas
    mars_facts_df = pd.read_html("https://space-facts.com/mars/")[0]
    mars_facts_df.columns = ['Info','Value']
    mars_facts_df.set_index('Info',inplace = True)
    return mars_facts_df.to_html(classes="table table-striped")

# Getting hemisphere images of Mars

def Mars_Hemispheres(browser):
    #Setting up Splinterto browse the website to capture images of Mars.

    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    #now visiting the website
    browser.visit(hemi_url)

    #Capturing the Hemisphere title and image url.
    hemisphere_image_urls = []

    links = browser.find_by_css("a.itemLink.product-item h3")

    for link in range(len(links)):
        browser.find_by_css("a.itemLink.product-item h3")[link].click()

        image_element = browser.find_link_by_text("Sample").first

        hemi_image_url = image_element["href"]

        hemi_title = browser.find_by_css("h2.title").text.replace(" Enhanced","")

        hemisphere_image_urls.append({"title" : hemi_title, 
                                      "img_url":hemi_image_url})
        browser.back()
    return hemisphere_image_urls

#Creating a comprehensive scraper and setting up a dictionary
def All_Scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    news_date, news_title, news_p =  NASA_mars_news(browser)   
    featured_image_url = jpl_image(browser)
    Mars_WX = Wx_Mars(browser)
    mars_facts_df = Mars_Facts()
    hemisphere_image_urls = Mars_Hemispheres(browser)


    mars_dict = {"News Date" : news_date,
                 "News Title": news_title,
                 "News Article": news_p,
                 "Featured Image": featured_image_url,
                 "Mars Weather": Mars_WX,
                 "Facts About Mars": mars_facts_df,
                 "Hemisphere Images": hemisphere_image_urls}
                
    browser.quit()
    return mars_dict

if __name__ == "__main__":
    print(All_Scrape())
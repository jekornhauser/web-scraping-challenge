#I couldn't figure out the scrape function so I copy pasted from csv

from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import re

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#Mars News
url ="https://mars.nasa.gov/news/"
browser.visit(url)

html=browser.html
soup = bs(html, "html.parser")

news_title = soup.find("div", class_="content_title").text
print(news_title)

news_p = soup.find("div", class_="article_teaser_body").text
print(news_p)

browser.quit()

#Featured Space Image
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url)
html=browser.html
soup = bs(html, "html.parser")

image = soup.find("div", class_="SearchResultCard-image").img["src"]

#Could not figure out how to isolate the .jpg from the div

browser.quit()

#Mars Facts
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
url = "https://space-facts.com/mars/"
browser.visit(url)
html=browser.html
soup = bs(html, "html.parser")

mars_facts_table = pd.read_html(url)[0]
print(mars_facts_table)

browser.quit()

#Mars Hemispheres
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
url = "https://webcache.googleusercontent.com/search?q=cache:Ljops39QW5MJ:https://astrogeology.usgs.gov/search/results%3Fq%3Dhemisphere%2Benhanced%26k1%3Dtarget%26v1%3DMars+&cd=2&hl=en&ct=clnk&gl=us"
browser.visit(url)
html=browser.html
soup = bs(html, "html.parser")

path = "//div[@class='description']//a[@class=class='itemLink product-item']/h3"
paths = browser.find_by_xpath(path)
print(paths)

#I was unable to grab the links no matter what I tried.  I ended up trying to go use regex.  The code I tried to use was:
x = soup.find_all("div", class_="description")
print(x)

#I then made a for loop and tried to use regex to grab the links from the text.
links = []
for i in range(4):
    result = re.findall(r'search.enhanced', x[i])
    links.append(result)
#this didn't work as regex works on strings and apparently i had a beautifulsoup object
#I was unable to convert this to a string

#How I would scrape if I had the links
hemisphere_image_urls = []
for i in links:
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://astrogeology.usgs.gov/" + links[i]
    browser.visit(url)
    html=browser.html
    soup = bs(html, "html.parser")
    hemisphere_image_urls.append({"title": soup.find("h2", class_="title").text, "image_url":soup.find("a", target_="_blank")["href"]})
    browser.quit()
#I was unable to test this code as it was all theoretical

site_urls=[]
for y in x:
    url = y.find('a')['href']
    site_urls.append(url)
print(site_urls)

hemisphere_image_urls = []
for i in range(4):
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = f"https://astrogeology.usgs.gov{site_urls[i]}"
    browser.visit(url)
    html=browser.html
    soup = bs(html, "html.parser")
    a = soup.find("div", class_="content")
    title = a.find('h2').text
    b = soup.find("div", class_="downloads")
    img_url = b.find('a')['href']
    print(img_url)
    hemisphere_image_urls.append({"title": title, "img_url": img_url})
    browser.quit()

print(hemisphere_image_urls)
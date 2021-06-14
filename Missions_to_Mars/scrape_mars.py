#Dependencies
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import json


def scrape_mars():

    scrape_list = {}

    #Splinter Setup

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    
    #Mars News

    url = 'https://redplanetscience.com'             
    browser.visit(url)
    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    article_headers = soup.find_all('div', class_='content_title')
    lateset_header = article_headers[0].text

    article_teasers = soup.find_all('div', class_='article_teaser_body')
    latest_teaser = article_teasers[0].text

    #JPL Images

    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_path = soup.find_all('img')[1]["src"]
    featured_image_url = url + image_path

    #Facts Table

    facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)
    tables = pd.read_html(facts_url)[0]

    facts_df = tables[0]
    facts_df.columns = facts_df.iloc[0]
    comparison = facts_df[1:]
    comparison.set_index('Mars - Earth Comparison')
    html_table = comparison.to_html()
    html_table.replace('\n', '')

    #Hemispheres

    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)

    soup = BeautifulSoup(browser.html, 'html.parser')
    items = soup.find_all('div', class_= 'description') 

    hemisphere_images = [] 
    for item in items: 

        itemtitle = item.find('div', class_='description').find('h3').text
        url = item.find('a')['href']
        full_url = 'https://marshemispheres.com/'
        image_url = full_url + url

        browser.visit(image_url)
        html = browser.html
        
        
        soup = BeautifulSoup(html, 'html.parser')
        image = soup.find('div', class_='downloads').find('ul')['href']
        final_image = full_url + image
        hemisphere_images.append({'title':itemtitle, 'img_url':final_image})
        
    browser.quit()

    data = {
        'lateset_header': lateset_header,
        'latest_teaser': latest_teaser,
        'featured_image_url': featured_image_url,
        'mars_facts': html_table,
        'hemisphere_images': hemisphere_images
    }
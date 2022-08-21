# Importing dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    url_main = 'https://redplanetscience.com/'
    browser.visit(url_main) 
    time.sleep(2)
    html_main = browser.html
    soup_main = BeautifulSoup(html_main, 'html.parser')

    main_news = soup_main.find('div', class_='content_title')
    news_title = main_news.text

    main_paragraph = soup_main.find('div', class_ = 'article_teaser_body')
    news_p = main_paragraph.text

    #Using splinter to find featured image
    url_img = 'https://spaceimages-mars.com/'
    browser.visit(url_img)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    feature_url = soup.find('img', class_='headerimage fade-in')
    feature_image_url = url_img + feature_url['src']

    #Scraping table with Pandas
    pandas_url = 'https://galaxyfacts-mars.com/'
    pandas_table = pd.read_html(pandas_url)
    df = pandas_table[1]
    #HTML table string
    mars_html_table = df.to_html()

    #Mars hemispheres
    url_main1 = 'https://marshemispheres.com/'
    browser.visit(url_main1) 

    section = browser.find_by_id('product-section')
    a_list = list(section.find_by_tag('a'))
    a_list2 = []
    for a in a_list:
        print(a['href'])
        if a['href'] not in a_list2:
            a_list2.append(a['href'])
        else:
            print(a)
            a.click()
            time.sleep(3)
            browser.back()
    t_list = list(section.find_by_tag('h3'))

    title_list = []
    for title in t_list:
        print(title.text)
        title_list.append(title.text)
    
    a_list3 = ['https://marshemispheres.com/images/full.jpg', 'https://marshemispheres.com/images/schiaparelli_enhanced-full.jpg', 'https://marshemispheres.com/images/syrtis_major_enhanced-full.jpg', 'https://marshemispheres.com/images/valles_marineris_enhanced-full.jpg']
    
    hemisphere_image_urls = dict(zip(title_list, a_list3))
    
    scraped_data = {
        'News_Title': news_title,
        'News_article': news_p,
        'Featured_Image_Urls': feature_image_url,
        'Mars_Table': mars_html_table,
        'Hemisphere_Image_Urls': hemisphere_image_urls
    }

    return scraped_data
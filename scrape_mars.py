import pandas as pd
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

def scrape_info():
    # set up splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # visit web page
    url = "https://redplanetscience.com/"
    browser.visit(url)
    time.sleep(1)

    # create html object and scrape into soup
    html = browser.html
    soup = bs(html, "html.parser")

    # identify div with article info
    soup.find("div", class_="list_text")

    # scrape article date, title, and teaser
    news_date = soup.find("div", class_="list_text").find("div", class_="list_date").text
    news_title = soup.find("div", class_="list_text").find("div", class_="content_title").text
    news_teaser = soup.find("div", class_="list_text").find("div", class_="article_teaser_body").text

    # visit web page
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    time.sleep(1)

    # create html object and scrape into soup
    html = browser.html
    soup = bs(html, "html.parser")

    # scrape featured image
    featured_image_url = url + soup.find("img", class_="headerimage fade-in")["src"]

    # grab tables from web page
    url = "https://galaxyfacts-mars.com/"
    dfs = pd.read_html(url)

    # put profile table in variable
    df_mars = dfs[1]
    df_mars.set_index(df_mars.columns[0], inplace=True)
    df_mars.index.name = None

    # convert df to html table
    mars_fact_table = df_mars.to_html(header=False)

    # visit web page
    url = "https://marshemispheres.com/"
    browser.visit(url)
    time.sleep(1)

    # create html object and scrape into soup
    html = browser.html
    soup = bs(html, "html.parser")

    # find div with image links
    descriptions = soup.find_all("div", class_='description')

    hemisphere_img_urls = []
    # loop through divs to get title and link to full-size images
    for desc in descriptions:
        title = desc.h3.text[:-9]
        hemi_url = url + desc.a['href']
        browser.visit(hemi_url)
        hemi_html = browser.html
        hemi_soup = bs(hemi_html, "html.parser")
        img_url = url + hemi_soup.find("img", class_="wide-image")['src']
        hemi_dict = {"title": title, "img_url": img_url}
        hemisphere_img_urls.append(hemi_dict)
    

    # put variables in dictionary
    mars_dict = {
                    "news_date": news_date, 
                    "news_title": news_title, 
                    "news_teaser": news_teaser,
                    "featured_image_url": featured_image_url,
                    "mars_fact_table": mars_fact_table,
                    "hemisphere_img_urls": hemisphere_img_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict
#-------------------------------------------------------------------------
# AUTHOR: Christopher Ernesto
# FILENAME: crawler.py
# SPECIFICATION: Crawls computer science department and stores all web pages in mongoDB until permanent faculty page is found
# FOR: CS 4250- Assignment #4
# TIME SPENT: 3 hours
#-----------------------------------------------------------*/

from pymongo import MongoClient
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin
from urllib.error import HTTPError
import re

def startCrawling():
    # connect to database
    db = connectDataBase()
    page = db.page

    # run crawler
    seed = ["https://www.cpp.edu/sci/computer-science/"]
    crawlerThread(page, seed)


def connectDataBase():

    # Create a database connection object using pymongo

    DB_NAME = "pages"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:

        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]

        return db

    except:
        print("Database not connected successfully")


def crawlerThread(con, seed=[]):
    count = 0
    frontier = seed     # list of urls to visit
    visitedSites = []   # list of visited urls

    while frontier:
        count += 1
        # get next URL
        url = frontier.pop(0)

        try:
            # open URL
            html = urlopen(url)
            # create beautifulsoup object
            bs = BeautifulSoup(html.read(), 'html.parser')
            # store html
            storeHTML(con, url, bs)
            # add url to visited
            visitedSites.append(url)

            # check if URL is target page
            if target_page(bs, html):
                print("Found target url at: ", url)
                # clear frontier
                frontier = []
            else:
                # add all urls to frontier
                links = bs.find_all('a', href=True)
                for link in links:
                    site = link.get('href')
                    # join URL
                    completeURL = urljoin("https://www.cpp.edu/", site)
                    # if url has been visited, don't add
                    if completeURL not in visitedSites:
                        frontier.append(completeURL)

        except HTTPError as e:
            print(e)
        except Exception as e:
            print(e)


def storeHTML(con, url, bs):
    page = {
        "url": url,
        "html": str(bs)
    }
    con.insert_one(page)


def target_page(bs, html):
    # get heading with class "cpp-h1"
    headingText = bs.find('h1', {'class': 'cpp-h1'})

    # if heading exists
    if headingText:
        if headingText.text == "Permanent Faculty":
            return True
        else:
            return False


if __name__ == '__main__':
    startCrawling()

#-------------------------------------------------------------------------
# AUTHOR: Christopher Ernesto
# FILENAME: parser.py
# SPECIFICATION: Parse permanent faculty page to get the name, title, office, phone, email, and website of all faculty members
# FOR: CS 4250- Assignment #4
# TIME SPENT: 3 hours
#-----------------------------------------------------------*/

from pymongo import MongoClient
from bs4 import BeautifulSoup

def startParsing():
    # connect to pages database
    db = connectPagesDataBase()
    page = db.page
    # get the page from the database
    html = getHTML(page)
    # create beautiful soup object
    bs = BeautifulSoup(html, 'html.parser')

    # connect to faculty database
    db = connectFacultyDataBase()
    members = db.members

    # add attributes to faculty database
    storeFaculty(members, bs)

def connectPagesDataBase():
    # Create a database connection object using pymongo

    DB_NAME = "pages"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:

        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]

        return db

    except:
        print("Pages Database not connected successfully")


def connectFacultyDataBase():
    # Create a database connection object using pymongo

    DB_NAME = "faculty"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:

        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]

        return db

    except:
        print("Faculty Database not connected successfully")


def getHTML(page):
    site = page.find_one({'url': 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'})
    html = site["html"]
    return html


def storeFaculty(members, bs):
    # get all sections
    facultySection = bs.find("section", {'class': 'text-images'}).find_all('div', {'class': 'clearfix'})
    for faculty in facultySection:
        # if section has a member
        if faculty.find('h2'):
            p = faculty.find('p')
            strong = p.find_all('strong')
            a = p.find_all('a')
            name = clean(faculty.find('h2').text)
            title = clean(strong[0].next_sibling.strip())
            office = clean(strong[1].next_sibling.strip())
            phone = clean(strong[2].next_sibling.strip())
            email = clean(a[0].text)
            website = clean(a[1].text)

            member = {
                "name": name,
                "title": title,
                "office": office,
                "phone": phone,
                "email": email,
                "website": website
            }

            print(member)
            members.insert_one(member)

def clean(text):
    ret = text.replace("&nbsp", "")
    ret = ret.replace(":", "")
    ret = ret.strip()
    return ret

if __name__ == '__main__':
    startParsing()
# CS4250_Assignment4

The solution for question 4 is in crawler.py.
The solution for question 5 is in parser.py

Crawler.py will start crawling from the seed URL: https://www.cpp.edu/sci/computer-science/. It wil find all links and go to each of them until the "Permanent Faculty" page is found. All links traversed are downlaoded into a MongoDB database.

Parser.py will parse the "Permanent Faculty" page to find the name, title, office, phone, email, and website of all faculty members. It stores the information in a mongoDB database called 'faculty' in the 'members' collection. 

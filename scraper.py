from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException

# A basic url for the WM Open Course List that can be added too
BASE_URL = "https://courselist.wm.edu/courselist/courseinfo/searchresults?term_code=202220&term_subj=&attr=0&attr2=0&levl=0&status=0&ptrm=0&search=Search"

# Scrapes the page for the given subject, finds the row (in table) with the given CRN and returns its status (open OR closed).
# param CRN: the unique identifier for the course in the given subject
# param subject: the subject to check for the course in
def checkStatus(CRN, subject):
    pass

# Determines the existence of the given params. Checks if the URL with the given subject exists. If so, checks if the given CRN exists on that URL.
# param CRN: the unique identifier for the course to check the existence of
# param subject: the subject to check the existence of
def checkValidity(CRN, subject):
    pass

# Creates a url for a subject page on the WM Open Course List
# param subject: the subject identifier to be inserted into the URL (Examples: CSCI, BIOL, THEA, etc)
def createURL(subject):
    insertLocStr = "term_subj="
    insertLocIndex = BASE_URL.find(insertLocStr)

    return BASE_URL[:insertLocIndex + 10] + subject + BASE_URL[insertLocIndex + 10:]

# Attempts to scrape a web page.
# param URL: the url to scrape
# return: the html code of the web page
# raise: exception if the URL doesn't exist or the request times out
def scrape(URL):
    try:
        source = requests.get(URL, timeout = 10.000)
    except requests.exceptions.RequestException as e:
        raise RequestException

    soup = BeautifulSoup(source.text, "lxml")

    # Checks if the url leads to a special error page
    if soup.find("h1", class_ = "bannerTitle").a.text.strip() == "Error":
        raise RequestException

    return soup

try:
    print(scrape(createURL("CSCI")))
except requests.exceptions.RequestException as e:
    print("AHHH! An error")
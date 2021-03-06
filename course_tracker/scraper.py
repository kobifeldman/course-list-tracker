import requests
from requests.exceptions import RequestException

from bs4 import BeautifulSoup

# The base url for the WM Open Course List that can be added too
BASE_URL = "https://courselist.wm.edu/courselist/courseinfo/searchresults?term_code=202310&term_subj=&attr=0&attr2=0&levl=0&status=0&ptrm=0&search=Search"

# Scrapes the page for the given subject, finds the row (in table) with the given CRN and returns its status (open OR closed).
# param CRN: the unique identifier for the course in the given subject
# param subject: the subject to check for the course in
# return: True if open, false if closed
# raise: RequestException if the URL does not exist or there is a problem retrieving it OR the CRN cannot be found
def checkStatus(CRN: int, subject: str) -> bool:
    try:
        soup = scrape(createURL(subject))
    except requests.exceptions.RequestException:
        raise RequestException

    # Retrieves all of the cells in the table as a list
    table = soup.find("div", id = "results").table.tbody
    cells = table.find_all("td")

    for index, cell in enumerate(cells):
        # If the cell being looked at contains a CRN
        if index % 11 == 0:
            if cell.text.strip() == str(CRN):
                # Checks the cell that contains the status for this specific CRN
                if cells[index + 10].text.strip() == "OPEN":
                    return True
                elif cells[index + 10].text.strip() == "CLOSED":
                    return False
    
    # If we go through entire loop and can't find the CRN
    raise RequestException

# Determines the existence of the given params. Checks if the URL with the given subject exists. If so, checks if the given CRN exists on that URL.
# param CRN: the unique identifier for the course to check the existence of
# param subject: the subject to check the existence of
# return: True if the CRN and URL exist, false if the URL exists but the CRN does not
# raise: RequestException if the URL does not exist or there is a problem retrieving it
def checkValidity(CRN: int, subject: str) -> bool:
    try:
        soup = scrape(createURL(subject))
    except requests.exceptions.RequestException:
        raise RequestException

    # Retrieves all of the cells in the table as a list
    table = soup.find("div", id = "results").table.tbody
    cells = table.find_all('td')

    for index, cell in enumerate(cells):
        # If the cell being looked at contains a CRN
        if index % 11 == 0:
            if cell.text.strip() == str(CRN):
                return True

    # If we go through entire loop and can't find the CRN
    return False

# Creates a url for a subject page on the WM Open Course List.
# param subject: the subject identifier to be inserted into the URL (Examples: CSCI, BIOL, THEA, etc)
# return: The URL
def createURL(subject: str) -> str:
    insertLocStr = "term_subj="
    insertLocIndex = BASE_URL.find(insertLocStr)

    return BASE_URL[:insertLocIndex + 10] + subject + BASE_URL[insertLocIndex + 10:]

# Attempts to scrape a subject page on the WM open course list site.
# param URL: the url to scrape
# return: the html code of the web page
# raise: RequestException if the URL does not exist or there is a problem retrieving it
def scrape(URL: str) -> BeautifulSoup:
    try:
        source = requests.get(URL, timeout = 10.000)
    except requests.exceptions.RequestException:
        raise RequestException

    soup = BeautifulSoup(source.text, "lxml")

    # Checks if the url leads to a special error page
    if soup.find("h1", class_ = "bannerTitle").a.text.strip() == "Error":
        raise RequestException

    return soup
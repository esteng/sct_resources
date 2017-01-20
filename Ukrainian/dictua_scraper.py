import sys
import requests
import urllib
import re
from bs4 import BeautifulSoup
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Origin': 'http://www.indiapost.gov.in',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko)  Chrome/24.0.1312.57 Safari/537.17',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': "http://lcorp.ulif.org.ua/dictua/",
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'
}

class MyOpener(urllib.request.FancyURLopener):
    version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17'

myopener = MyOpener()
url = "http://lcorp.ulif.org.ua/dictua/"

f=  myopener.open(url)
soup = BeautifulSoup(f,'lxml')

viewstate = soup.select("#__VIEWSTATE")[0]['value']
eventvalidation = soup.select("#__EVENTVALIDATION")[0]['value']

formData = (
    ('__EVENTVALIDATION', eventvalidation),
    ('__VIEWSTATE', viewstate),
    ('__VIEWSTATEENCRYPTED',''),
    ('ctl00_ContentPlaceHolder1_tsearch','слова'),
    ('ctl00_ContentPlaceHolder1_search','')
)
    # ('ctl00$ContentPlaceHolder1$tsearch','слова'),
    # ('ctl00_ContentPlaceHolder1_search','')

encodedFields = urllib.parse.urlencode(formData)
f = myopener.open(url, encodedFields)

with open("test.html",'w') as f1:
    f1.writelines([x.decode('utf8') for x in f.readlines()])
span_regex = re.compile("<span class=\"word_style\" >.*</span>")

def search_word(word):

    url = "http://lcorp.ulif.org.ua/dictua/"


    # soup = BeautifulSoup(result, "html.parser")
    # span = span_regex.search(result)
    # if span is not None:
    #     s = span.group(0)
    #     print(s)




search_word("слова")
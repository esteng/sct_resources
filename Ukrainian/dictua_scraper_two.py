import re
import requests
from urllib.request import FancyURLopener
import http.client
from bs4 import BeautifulSoup
from collections import defaultdict
from time import sleep
 

HEADERS = {
"Host": "lcorp.ulif.org.ua",
"Connection": "keep-alive",
"Content-Length": "10901",
"Cache-Control": "no-cache",
"Origin": "http://lcorp.ulif.org.ua",
"X-MicrosoftAjax": "Delta=true",
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
"Content-Type": "application/x-www-form-urlencoded",
"Accept": "*/*",
"Referer": "http://lcorp.ulif.org.ua/dictua/",
"Accept-Encoding": "gzip, deflate",
"Accept-Language": "en-US,en;q=0.8",
"Cookie": "SESS86f0a93a60b489e31e9d907b879bdad1=avr2c3uc42jtckdt0tnv64gpb7; ASP.NET_SessionId=mmaz0xvj3fhd0045soyqiy45"
}


vowels = ["а", "е", "є", "и", "і", "ї", "о", "у", "ю", "я"]
ord_vowels = [ord(x) for x in vowels]

class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17'

myopener = MyOpener()
url = "http://lcorp.ulif.org.ua/dictua/"

f=  myopener.open(url)
soup = BeautifulSoup(f,'lxml')

stress_dict = defaultdict()

viewstate = soup.select("#__VIEWSTATE")[0]['value']


def get_word_html(word):

    pay = {"ctl00$ContentPlaceHolder1$ScriptManager1":"ctl00$ContentPlaceHolder1$UpdText|ctl00$ContentPlaceHolder1$search",
    "__EVENTTARGET":"ctl00$ContentPlaceHolder1$dgv",
    "__EVENTARGUMENT":"Select$21",
    "__VIEWSTATE" : viewstate,
    "__VIEWSTATEGENERATOR": soup.select("#__VIEWSTATEGENERATOR")[0]['value'],
    "__EVENTVALIDATION": soup.select("#__EVENTVALIDATION")[0]['value'],
    "ctl00$ContentPlaceHolder1$tsearch": word,
    "ctl00$ContentPlaceHolder1$search.x":"29",
    "ctl00$ContentPlaceHolder1$search.y":"13"}

    r = requests.post(url, data = pay, headers = HEADERS)

    return r.text

def parse_html(html):
    all_words = set()
    spanregex = "(<span.*>)|(<\/span>)"
    tdregex = "(<td.*>)|(<\/td>)"

    soup = BeautifulSoup(html,'lxml')

    word_trans_list = soup.find_all("span",'word_style')
    declension_trans_list = soup.find_all("td","td_inner_style")

    for span in word_trans_list:
        nospan = re.sub(spanregex, "", str(span))
        splitup = re.split(',', nospan)
        splitup = [x.strip() for x in splitup]
        all_words |= set(splitup)
    for td in declension_trans_list:
        notd = re.sub(tdregex, "", str(td))
        tdsplitup = re.split(',', notd)
        tdsplitup = [x.strip() for x in tdsplitup]
        all_words |= set(tdsplitup)
    
    just_words = list(all_words)
    return just_words


def make_stress_pattern(word, stressed):
    pattern = ""
    for j, char in enumerate(word):
        if char in vowels and j!= stressed:
            pattern +='0'
        elif char in vowels and j == stressed:
            pattern += '1'
    return pattern

def get_stress(words):
    

    for word in words:
        if word!='':
            for i, char in enumerate(word):
                if char == u"\u0301":
                    stressed = i-1
                    word = re.sub(u"\u0301", "", word)
                    stress_pattern = make_stress_pattern(word, stressed)
                    with open("stresses_from_dictua.txt",'a') as f3:   
                        f3.write(word+ " "+stress_pattern+"\n")
                    # print("adding ", word, ' : ', stress_pattern)
                    stress_dict[word] = stress_pattern
                    

def get_all_words():
    with open('uk_full.txt') as f1:
        lines = f1.readlines()
    words = [re.split("\s", x)[0].strip() for x in lines]
    for i,word in enumerate(words):
        if i%100 == 0:
            print("{} % done".format(i/len(words)*100))
        try:
            get_stress(parse_html(get_word_html(word)))
            sleep(.1)
        except:
            pass

get_all_words()
with open("stresses_from_dictua_dict.txt",'w') as f3:
    for key, entry in stress_dict.items():
        f3.write(key, " ", entry, "\n")

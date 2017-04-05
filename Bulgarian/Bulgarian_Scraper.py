import requests
import re
import csv
import time
from bs4 import BeautifulSoup


def get_html(word):
    url = "http://ibl.bas.bg/dictionary_portal/lang/bg/all/{}".format(word)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.find_all('blockquote')[0]

def search_word(word, quote):
    if quote == None:
        return None
    all_possible = permute_accent(word)
    for poss in all_possible:
        reg = re.compile(poss)
        m = reg.search(quote.text)
        if m is not None:
            return m.group(0)


def permute_accent(word):
    vowels = ['и', 'е', 'у', 'о', 'ъ', 'а']
    all_perms= []
    vowel_regex = re.compile("["+"".join(vowels) + "]")
    all_vowels = vowel_regex.finditer(word)
    for match in all_vowels:

        current_word  = word[0:match.start()] +word[match.start()]  + u"\u0300" + word[match.end():]
        all_perms.append(current_word)

    return all_perms


def get_stress_pattern(word):
    vowels = ['и', 'е', 'у', 'о', 'ъ', 'а']
    pat = ""
    if word is None:
        return
    for i,c in enumerate(list(word)):
        try:
            if c in vowels and word[i+1] !=  u"\u0300":
                pat +='0'
            if c in vowels and word[i+1] ==  u"\u0300":
                pat += '1'
                continue
        except IndexError:
            if c in vowels:
                pat += '0'
            else:
                continue
    return pat


def get_all():
    all_stress = {}
    with open("bg_full.txt") as f1:
        lines = f1.readlines()
    for line in lines:
        word = re.split("\s", line)[0]
        stressed_word = search_word(word, get_html(word))
        stress_pattern = get_stress_pattern(stressed_word)
        if stress_pattern is not None:
            all_stress.update({word: stress_pattern})
        time.sleep(0.01)
    return all_stress

all_dict = get_all()
print(len(all_dict))
with open("stresses.txt", "w") as f2:
    for k,v in all_dict.items():
        f2.write(k.strip() + "\t" + v.strip() + "\n")


# html = get_html("имаме")
# print(search_word("имаме", html), " found")
# print(get_stress_pattern(search_word("имаме", html)))
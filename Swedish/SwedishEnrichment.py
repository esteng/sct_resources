import sys
import re
import csv
import urllib.request

"""
Frequency info from https://github.com/hermitdave/FrequencyWords/

word type information gotten from wiktionary (https://en.wiktionary.org/wiki/Category:Swedish_lemmas)

pronouns, prepositions, and conjunctions are function words, all others are content
"""

words = {}
def getHTML(page):
    """ get raw html from page"""
    with urllib.request.urlopen(page) as response:
        html = response.read().decode('utf-8')
    return html

def get_function_words():
	functionwords = []
	conjhtml = str(getHTML('https://en.wiktionary.org/wiki/Category:Swedish_conjunctions'))
	prephtml = str(getHTML('https://en.wiktionary.org/wiki/Category:Swedish_prepositions'))
	pronhtml = str(getHTML('https://en.wiktionary.org/wiki/Category:Swedish_pronouns'))

	regex = re.compile('<li><a href="\/wiki\/.*?" title=".*?">.*?<\/a><\/li>')

	conjmatches = regex.findall(conjhtml)
	prepmatches = regex.findall(prephtml)
	pronmatches = regex.findall(pronhtml)

	wordregex = re.compile("\">.+?<")

	for match in (conjmatches+pronmatches+prepmatches):
		rmatch = wordregex.search(match).group(0)
		functionwords.append(rmatch[2:-1])


	for word in functionwords:
		if 'Swedish' in word or 'lemmas' in word or 'by' in word or word == 'Prepositions by language':
			functionwords.remove(word)


	return(set(functionwords))

def getFrequency(path):
	with open(path,errors='ignore') as f:
		lines = f.readlines()
	total = sum([int(re.split('\s', x)[1]) for x in lines])

	for line in lines:
		splitline = re.split('\s', line)
		
		word = splitline[0]
		
		freq = (int(splitline[1])/total)*1000000

		
		words[word] = [freq, None]

def getPitchAccent(path):
    # 1 corresponds to acute, 2 to grave
    one = re.compile('^"(?!")')
    two = re.compile('^"".*')
    with open(path, errors='ignore') as f2:
        pitchlines = f2.readlines()
    for line in pitchlines:
        split = line.split(";")
       
        transcription = split[11].strip()
        word = split[0].strip()
        sequence = ""
        syllables = transcription.split("$")
        for syl in syllables:
            if one.match(syl.strip()):
                sequence += "1"
            elif two.match(syl.strip()):
                sequence+="2"
            else:
                sequence+="0"
        try:
        	# currently just replacing with most recent pitch accent, might be better ways to do this
            words[word][1] = sequence
        except KeyError:
            words[word] = [None, sequence]
        # print(line) if word == 'Sol' else 3



fwords= get_function_words()
getFrequency('sv_full.txt')
getPitchAccent("NST svensk leksikon/swe030224NST.pron/swe030224NST.pron")
f2 = open('SwedishEnrichmentData.csv', 'w')
f2CW = csv.writer(f2)
f2CW.writerow(['word','word type','frequency', 'pitch accent'])


for k,v in words.items():
	if k in fwords:
		wordtype = 'function'
	else:
		wordtype = 'content'
	f2CW.writerow([k,wordtype, v[0], v[1]])

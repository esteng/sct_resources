import re
import math
import urllib.request, urllib.parse
import multiprocessing
from multiprocessing import Process, Pool, Queue, Manager
import time
import sys
import os
import csv


##############
### README ###
##############
# Requires python 3.5+
# command line call:
# python scraper.py <language> <wordfile> <vowels> <batch>
# where: 
# <language> is the name of the language 
# <wordfile> is a file of words where the 1st element on each line is a word
# <vowels> is a string of all the vowels in IPA format in the language. EX: aeioueěêêǐǒ
# <batch> is how many batches you want to split the word file into. Default is the cpu count



lang = sys.argv[1]
wordfile = sys.argv[2]
vowels = sys.argv[3]

try:
	batch = sys.argv[4]
except IndexError:
	batch = multiprocessing.cpu_count()

print(batch)

def get_lines():
	
	lines = []

	with open(wordfile) as f2:
		originallines = f2.readlines()
	for line in originallines:
		word = re.split("\s", line)[0].replace("\"","")
		lines.append(word)
	return lines
	

	# get_words(lines, 10)
def getHTML(page):
    """ get raw html from page"""
    page = urllib.parse.urlsplit(page)
    page = list(page)
    page[2] = urllib.parse.quote(page[2])
    page = urllib.parse.urlunsplit(page)
    html = None
    try:
    	with urllib.request.urlopen(page) as response:
        	html = response.read().decode('utf-8')
    except:
    	pass
    return html


def get_words(q, lines, writenum=0):#(start=0,end=0, writenum = 0, queue = None):
	#words = queue.get()
	#print("starting from {} going to {}".format(start,end))
	iparegex = re.compile("span class=\"IPA\">.*<\/span")
	splitregex = re.compile("[<>]")
	vowelregex = re.compile('[{}]'.format(vowels))
	
	# f3 = open("stresses{}.txt".format(writenum), 'w')
	skipped = 0
	toret = {}
	#i = start
	for i in range(len(lines)):
		line = lines[i]
		html = getHTML('https://en.wiktionary.org/wiki/{}#{}'.format(line.strip().replace(' ','_'),lang))

		if html == None:
			skipped+=1
			continue
		all_ipa = iparegex.findall(str(html))
		for string in all_ipa:
			split = splitregex.split(string)
			ipa = re.sub("[\[\]]", "",split[1])
			just_vs = re.sub('[^ˌˈ{}]'.format(vowels),"",ipa)
			#get just vowels and stress marks
			stresspattern = ""

			viter = iter(just_vs)
			for seg in viter:
				#for each vowel or stressmark
				if seg == 'ˈ':
					stresspattern+='1'
					try:
						next(viter)
					except StopIteration:
						pass
				elif seg == 'ˌ':
					stresspattern+='2'
					try:
						next(viter)
					except StopIteration:
						pass
				else:
					stresspattern+='0'
			line = line.strip()

			#print("{},{}".format(line,stresspattern))
			#words[line] = stresspattern
			# f3.write("{},{}\n".format(line,stresspattern))
			if("1" in stresspattern):
				print("found 1")
			toret[line] = stresspattern
			# if i%100 == 0:
			# 	print("{} is {} percent done".format(multiprocessing.current_process().name, (i/len(lines))*100))
			time.sleep(.0001)
	q.put(toret)
	# f3.close()



if __name__ == "__main__":
	q = Queue()
	
	lines = get_lines()
	jobs = []
	step = math.floor(len(lines)/int(batch))

	print("there are {} processes".format(len(["x" for i in range(0, len(lines), step)])))



	for i in range(0, len(lines), step):
		p = Process(target = get_words, args = (q, lines[i:i+step]))
		jobs.append(p)
	
	for i, proc in enumerate(jobs):
		print('starting proc {}'.format(i))
		proc.start()

	for i,proc in enumerate(jobs):
		print('finishing proc {}'.format(i))
		proc.join()

	results = [q.get() for i in range(0, len(lines), step)]
	f3 = open("stresses.txt", "w")
	f3cw = csv.writer(f3, delimiter = " ")
	f3cw.writerow(["word","stress pattern"])
	for d in results:
		for k,v in d.items():
			f3cw.writerow([k, v])




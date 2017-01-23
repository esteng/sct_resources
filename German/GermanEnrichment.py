import csv
"""
Stress and word type information from: CELEX
Frequency information from: Subtlex-DE (http://crr.ugent.be/archives/534)



dict format:
word:[stress,frequency,word type]
"""

#replaces ae, oe, ue with umlauts
def replaceUmlaut(string): 
	string = string.replace("ae", "ä")
	if "euer" not in string:
		string = string.replace("ue", "ü")
	string = string.replace("oe", "ö")
	return string
#replace ss with ß
def replaceSharp(string):
	oldString = string
	string = string.replace("ss", "ß")
	if oldString is string:
		return ""
	return string

def replaceSubtlex(word):


	word = word.replace('-ae-', 'ä')
	word = word.replace('-oe-', 'ö')
	word = word.replace('-ue-', 'ü')

	
	return word

words = {}

def getStress(path):
	with open(path , "r") as f1:
		lines = f1.readlines()
	
		for line in lines:
			split = line.split("\\")
			stressed = split[4] #this is the part w ' and -
			ortho = replaceUmlaut(split[1])
			Sortho = replaceSharp(ortho)
			syls = stressed.split("-") #split into syllables
			numString = ""
			numSyls = len(syls)
			index= 0
			for i in range(len(syls)):
				if "'" in syls[i]:
					numString = numString + "1"
					index = i+1
				else:
					numString = numString + "0"
			if numString == "":
				numString = None
			words[ortho] = [numString, None, None]

			if Sortho is not "":
				words[Sortho] = [numString, None, None]
		
def getWordType(path):
	with open(path, "r") as f1:
		lines = f1.readlines()
		for line in lines:
			split = line.split("\\")
			sharp = ""
			if split[3] in {"3", "5", "6", "8"}:
				split[1] = replaceUmlaut(split[1])
				sharp = replaceSharp(split[1])
				try:
					words[split[1]][2] = "Function"
				except KeyError:
					words[split[1]] = [None, None, "Function"]
					#print(split[1])
				
				if sharp is not "":
					try:
						words[sharp][2] = "Function"
					except KeyError:
						words[sharp] = [None,None,"Function"]
						#print(sharp)
			else:
				try:
					words[split[1]][2] = "Content"
				except KeyError:
					words[split[1]] = [None,None,"Content"]
					#print(split[1])
				
				if sharp is not "":
					try:
						words[sharp][2] = "Content"
					except KeyError:
						words[sharp] = [None,None,"Content"]
						#print(sharp)

	

def getFrequency(path):
	with open(path,"r", encoding='utf-8',errors='ignore') as f1:
		lines = f1.readlines()
		for line in lines:
			split = line.split("\t")

			word = replaceSubtlex(split[0])
			# if word != split[0]:
			# 	print(word,split[0])

			try:
				words[word][1] = split[4].replace(",",".")
			except KeyError:
				words[word] = [None, split[4].replace(",","."), None]
				#print(word)

getStress("gpw.cd")
getWordType("gsl.cd")
getFrequency('SUBTLEX-DE.txt')

f2 = open("GermanEnrichmentData.csv", 'w')
f2cw = csv.writer(f2)


f2cw.writerow(['word','stress pattern','frequency','word type'])
for k,v in words.items():
	if v[2] in [None, ""]:
		v[2] = "Content"
	f2cw.writerow([k,v[0],v[1],v[2]])




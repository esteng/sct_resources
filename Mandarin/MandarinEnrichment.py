#!/usr/bin/bash
#encoding: utf-8

import re
import csv
import os

def get_function(path):
    function_words = list()
    lines = []
    for p in os.walk(path):
        for filename in p[2]:
            with open(os.path.join(p[0],filename))	as f1:
                lines.extend(f1.readlines())

    for line in lines:
        line = line.replace('"', "")
        splitline = line.split(",")
        word = splitline[1]
        if word.strip() == "细":
            print("found inside getfunctioon")
        function_words.append(word.strip())

    
    print(list(function_words))
    return function_words

def get_pinyin(path):
    toret = []

    trad = {}
    simp = {}
    with open(path) as f1:
        lines = f1.readlines()
    for line in lines:
        firstsecond = line.split("[")
        try:
            first = firstsecond[0]
            second = firstsecond[1]
        except IndexError:
            continue
        pinyin = second.split("]")[0].strip()
        traditional = first.split(" ")[0].strip()
        simplified = first.split(" ")[1].strip()
        just_tone = re.sub("[^0-9]","", pinyin).strip()
        trad[traditional] = (just_tone, pinyin)
        simp[simplified] = (just_tone, pinyin)

    toret.extend((trad, simp))
    return toret


def get_frequency(path):
    words ={}
    with open(path,errors='ignore') as f:
        lines = f.readlines()
    total = sum([int(re.split('\s', x)[1]) for x in lines])

    for line in lines:
        splitline = re.split('\s', line)
        
        word = splitline[0]
        
        freq = (int(splitline[1])/total)*1000000

        
        words[word] = freq
    return words
if __name__ == "__main__":



    function_words = get_function("/Users/elias/sct_resources/Mandarin/function")

    # pinyins = get_pinyin("/Users/elias/sct_resources/Mandarin/cedict_ts.u8")
    frequencies = get_frequency("/Users/elias/sct_resources/Mandarin/zh_full.txt")

    f1 = open("/Users/elias/sct_resources/Mandarin/MandarinEnrichmentData.csv","w")
    f1cw = csv.writer(f1)
    f1cw.writerow(['word','frequency','word type', 'tone', 'pinyin'])

    
    t,s=0,0
    for k,v in frequencies.items():
        towrite = []
        # simplewrite = []
        
        if k in function_words:
            word_type = "Function"
        else:
            word_type = "Content"
        towrite.extend((k,v,word_type))
        # simplewrite.extend((k,v,word_type))
        # d = pinyins[0]
        # try:
        #     #get traditional
        #     t+=1
        #     tone = d[k][0]
        #     pinyin = d[k][1]
        #     towrite.extend((tone,pinyin))
        # except KeyError:
        #     towrite.extend((None,None))
        # d = pinyins[1]
        # try:
        #     s+=1
        #     #get simplified
        #     tone = d[k][0]
        #     pinyin = d[k][1]
        #     simplewrite.extend((tone,pinyin))
        # except KeyError:
        #     simplewrite.extend((None,None))

        # if (towrite[3] == None and simplewrite[3] == None) or (towrite[3] != None and simplewrite[3] == None):
        #     f1cw.writerow(towrite)
        # elif towrite[3] == None and simplewrite[3] != None:
        #     f1cw.writerow(simplewrite)
        # else:
        #     f1cw.writerow(towrite)
        #     f1cw.writerow(simplewrite)
        f1cw.writerow(towrite)
    print("{} traditional words have pinyin/tone, {} simplified words have pinyin, tone".format(t,s))









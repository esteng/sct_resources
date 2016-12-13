import re


midgex = re.compile('.*(?<!;)\"\"')
ipawords = set()

with open("allipa.csv") as f1:
    ipalines = f1.readlines()

with open("NST svensk leksikon/swe030224NST.pron/swe030224NST.pron", errors='ignore') as f2:
    data = f2.readlines()

for line in ipalines:
    line = line.replace("\"","")
    splitline = line.split(",")
    ipawords.update(splitline[1])

for line in data:
    split = line.split(";")

    if midgex.search(split[11])!=None:
        if split[0].strip() in ipawords:
            print("found one: {}".format(split[0]))
            
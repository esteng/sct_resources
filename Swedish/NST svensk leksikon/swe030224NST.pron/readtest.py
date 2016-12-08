#  !/usr/bin/python
# -*- coding: utf-8  -*-


allphones1 = set()
with open("swe030224NST.pron",encoding='utf-8', errors='ignore') as f1:
    lines = f1.readlines()

count =0

splitlines = [x.split(";") for x in lines]

for s in splitlines:
    [allphones1.update(x) for x in s[11].split()]

    if "%" not in s[11]:
        count+=1
        print(s[11])


print("{} dont have % out of {}, {}%".format(count, len(lines), count/len(lines)))
# print(allphones1)


# allphones2 = set()
# with open("swe030224NST.pron",encoding='utf-8', errors='replace') as f1:
#     lines = f1.readlines()



# splitlines = [x.split(";") for x in lines]

# for s in splitlines:
#     [allphones2.update(x) for x in s[11].split()]



# missing = allphones2-allphones1

# print(ord(list(missing)[0]))


# with open("swe030224NST.pron",encoding='utf-8', errors='strict') as f:
#     string = ""
#     while True:
#         try:
#             c = f.read(1)
#             string+=c
#         except UnicodeError:
#             print(string)
#             break
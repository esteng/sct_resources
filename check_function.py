import os 
import csv




for d in os.walk('/Users/elias/sct_resources'):
    for filename in d[2]:
        if filename.endswith("Data.csv"):
            with open(os.path.join(d[0],filename)) as f1:
                reader= csv.DictReader(f1)
                count = 0
                for row in reader:
                    try:
                        if row['word type'] in ["", None, "None", "null", "Null"]:
                            count+=1
                    except KeyError:
                        print("filename {} does not have 'word type'".format(filename))
                        break
                print("in filename {} there are {} rows missing 'word type'".format(filename, count))

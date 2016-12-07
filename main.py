import Readability.DCReadability as DCR
from nltk.stem.porter import *
import os
import csv

entries = [ f for f in os.listdir('data/content1') ]
names = [ f for f in os.listdir('data/ref1') ]
os.remove('readRes.csv')
output = open('readRes.csv', 'wb')
fieldnames = ['file', 'Publisher', 'Readability']
writer = csv.DictWriter(output, fieldnames=fieldnames)
writer.writeheader()

#create dict
commonWordsFile = open("Readability/The_Dale-Chall_Word_List.txt", "r")
cw= commonWordsFile.readlines()
dict={}
#cw=unicode(cw,'utf-8')
stemmer = PorterStemmer()
for w in cw:
    ws=stemmer.stem(unicode(w,'utf-8'))
    dict[ws]=1
commonWordsFile.close()
i=0
for e in entries:
    textfile = open(os.path.join('data/content1',e), "r")
    reffile = open(os.path.join('data/ref1',names[i]), "r")
    text = textfile.read()
    try:
        grade = DCR.grade(text, dict)
        writer.writerow({'file': e,'Publisher': reffile.readline()[:-1], 'Readability': grade})
    except UnicodeDecodeError:
        #textfile.close()
        #os.remove(os.path.join('data/content1',e))
        print "skip", e
    textfile.close()
    reffile.close()
    i=i+1

output.close()
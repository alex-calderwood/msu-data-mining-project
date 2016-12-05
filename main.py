import Readability.DCReadability as DCR
from nltk.stem.porter import *
import os

entries = [ f for f in os.listdir('data/content1') ]
print entries[0],entries[1]

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
for e in entries:
    textfile = open(os.path.join('data/content1',e), "r")
    text = textfile.read()
    print e, DCR.grade(text, dict)
    textfile.close()
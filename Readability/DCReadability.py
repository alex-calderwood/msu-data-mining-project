#import nltk
#nltk.download('porter_test')
from __future__ import division
from nltk.stem.porter import *
from nltk.tokenize import sent_tokenize, word_tokenize

#somehow this fixes rootword in w
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

def grade(doc):
    stemmer = PorterStemmer()
    commonWordsFile = open("Readability/The_Dale-Chall_Word_List.txt", "r")
    cw= commonWordsFile.readlines()
    i=0
    dict={}
    #cw=unicode(cw,'utf-8')
    for w in cw:
        ws=stemmer.stem(unicode(w,'utf-8'))
        dict[ws]=1

    sentences = sent_tokenize(doc)
    words = word_tokenize(doc)
    ASL = len(words)/len(sentences)-1 #-1 for each period
    i=0
    
    for word in words:
        rootWord = stemmer.stem(word)
        if dict.has_key(rootWord):
            i=i+1
    DS = 1-i/(len(words)-len(sentences))
    RGS = (0.1579 * DS) + (0.0496 * ASL)
    if DS>.05:
        RGS=RGS + 3.6365
    print "reading grade is:",RGS

    commonWordsFile.close()
    return

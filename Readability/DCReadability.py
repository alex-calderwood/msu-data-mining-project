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
    commonWordsFile = open("Readability/The_Dale-Chall_Word_List.txt", "r")
    cw= commonWordsFile.readlines()

    sentences = sent_tokenize(doc)
    words = word_tokenize(doc)
    ASL = len(words)/len(sentences)-1 #-1 for each period
    i=0
    stemmer = PorterStemmer()
    for word in words:
        rootWord = stemmer.stem(word)
        if any(rootWord in w for w in cw):
            i=i+1
    DS = 1-i/(len(words)-len(sentences))
    RGS = (0.1579 * DS) + (0.0496 * ASL) + 3.6365
    print "reading grade is:",RGS

    commonWordsFile.close()
    return

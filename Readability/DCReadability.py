#import nltk
#nltk.download('porter_test')
from __future__ import division
from nltk.stem.porter import *
from nltk.tokenize import sent_tokenize, word_tokenize

#somehow this fixes rootword in w
import sys  
reload(sys)  
#sys.setdefaultencoding('utf8')

def grade(doc, dict):
    stemmer = PorterStemmer()
    i=0

    sentences = sent_tokenize(doc)
    words = word_tokenize(doc)
    ASL = len(words)/len(sentences)-1 #-1 for each period
    i=0
    
    for word in words:
        rootWord = stemmer.stem(unicode(word,'utf-8'))
        if dict.has_key(rootWord):
            i=i+1
    DS = 1-i/(len(words)-len(sentences))
    RGS = (0.1579 * DS) + (0.0496 * ASL)
    if DS>.05:
        RGS=RGS + 3.6365
    #print "reading grade is:",RGS

    return RGS

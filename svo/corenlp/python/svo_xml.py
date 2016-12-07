from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
stopwords = set(stopwords.words('english'))

import verb_net_reader
import file_tools

xmlPath = "../../../data/xml/"

debug = True
debugXML = False


def getSPOTuples(xmlRoot):
    subjects = []
    predicates = []
    objects = []

    for sentenceNode in xmlRoot.find('document').find('sentences').findall('sentence'):
        for openie in sentenceNode.findall('openie'):
            for tripleNode in openie.findall('triple'):
                subjectNode = tripleNode.find('subject')
                predNode = tripleNode.find('relation')
                objectNode = tripleNode.find('object')

                subjects.append(subjectNode.find('text').text)
                predicates.append(predNode.find('text').text)
                objects.append(objectNode.find('text').text)

    return subjects, predicates, objects


def listTokenFrequencies(tokenList):
    if tokenList is None:
        return

    freqDict = {}

    for token in tokenList:
        if freqDict.get(token) is None:
            freqDict[token] = 1
        else:
            freqDict[token] += 1

    print(freqDict)


def getPoliticianOccurances(tokenList):
    trumpTripleIndices = []
    clintonTripleIndices = []

    for i in range(len(tokenList)):
        text = tokenList[i]
        if 'Trump' in text or 'Donald' in text:
            trumpTripleIndices.append(i)
        elif 'Clinton' in text or 'Hillary' in text:
            clintonTripleIndices.append(i)

    print("Trump: ", len(trumpTripleIndices), "Clinton:", len(clintonTripleIndices))
    return trumpTripleIndices, clintonTripleIndices

def getTokensFromList(indicesToExtract, textList):
    tokens = []
    for i in indicesToExtract:
        for token in word_tokenize(textList[i]):
            token = token.lower()
            if token not in stopwords:
                tokens.append(token)
    return tokens


def doSvoAnalysis(fileName):
    root = file_tools.getXMLRoot(fileName)
    subjects, predicates, objects = getSPOTuples(root)
    
    if(debugXML):
        print(subjects)
        print(predicates)
        print(objects)
        
    indicesOfTrumpSubs, indicesOfClintonSubs = getPoliticianOccurances(subjects)
    getPoliticianOccurances(predicates)
    getPoliticianOccurances(objects)
    
    trumpPreds = []
    trumpObjs = []
    trumpSubjs = []
    
    print('\nTrump Triples:')
    for tripleIndex in indicesOfTrumpSubs:
        print(subjects[tripleIndex], '|', predicates[tripleIndex], '|', objects[tripleIndex])
        trumpPreds.append(predicates[tripleIndex])
        trumpObjs.append(objects[tripleIndex])
        trumpSubjs.append(subjects[tripleIndex])

    # # Print out the frequencies of tokens that occur as predicates when Trump occurs in the subject
    # print('Trump Predicate Frequencies:')
    # print(listTokenFrequencies(getTokensFromList(indicesOfTrumpSubs, predicates)))
    # # Print out the frequencies of tokens that occur as objects when Trump occurs in the subject
    # print('Trump Object Frequencies:')
    # print(listTokenFrequencies(getTokensFromList(indicesOfTrumpSubs, objects)))
    
    
    # Do the same thing for Clinton TODO: Extract this to a function
    clintonPreds = []
    clintonObjs = []
    clintonSubjs = []
    print('\nClinton Triples:')
    for tripleIndex in indicesOfClintonSubs:
        print(subjects[tripleIndex], '|', predicates[tripleIndex], '|', objects[tripleIndex])
        clintonPreds.append(predicates[tripleIndex])
        clintonObjs.append(objects[tripleIndex])
        clintonSubjs.append(subjects[tripleIndex])

    return (trumpSubjs, trumpPreds, trumpObjs, clintonSubjs, clintonPreds, clintonObjs)

    # # Print out the frequencies of tokens that occur as predicates when Clinton occurs in the subject
    # print('Clinton Predicate Frequencies:')
    # print(listTokenFrequencies(getTokensFromList(indicesOfClintonSubs, predicates)))
    # # Print out the frequencies of tokens that occur as objects when Clinton occurs in the subject
    # print('Clinton Object Frequencies:')
    # print(listTokenFrequencies(getTokensFromList(indicesOfClintonSubs, objects)))


if __name__ == '__main__':
    # Store verbnet xml in usable python dict format
    print('--- Reading verbnet files ---')
    verbNet = verb_net_reader.VerbNet()
    verbNet.readVerbnetFiles()
    verbNet.print()
    print()

    xmlFiles = file_tools.getFilesFrom(xmlPath)
    print(xmlFiles)
    for file in xmlFiles:
        doSvoAnalysis(xmlPath + file)
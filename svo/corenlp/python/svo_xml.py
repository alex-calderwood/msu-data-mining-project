import xml.etree.ElementTree as ET
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))

def getXMLRoot(xmlFileName):
    xmlTree = ET.parse(xmlFileName)
    xmlRoot = xmlTree.getroot()
    return xmlRoot


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




def occurances(tokenList):
    trumpTripleIndices = []
    clintonTripleIndices = []

    for i in range(len(tokenList)):
        text = tokenList[i]
        if 'Trump' in text:
            trumpTripleIndices.append(i)
        elif 'Clinton' in text:
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


if __name__ == '__main__':
    fileName = "test.xml"
    root = getXMLRoot(fileName)
    subjects, predicates, objects = getSPOTuples(root)

    print(subjects)
    indicesOfTrumpSubs, indicesOfClintonSubs = occurances(subjects)

    print(predicates)
    occurances(predicates)

    print(objects)
    occurances(objects)


    trumpPreds = []
    trumpObjs = []
    print('\nTrump Triples:')
    for tripleIndex in indicesOfTrumpSubs:
        print(subjects[tripleIndex], '|', predicates[tripleIndex], '|', objects[tripleIndex])
        trumpPreds.append(predicates[tripleIndex])
        trumpObjs.append(predicates[tripleIndex])

    # Print out the frequencies of tokens that occur as predicates when Trump occurs in the subject
    print('Trump Predicate Frequencies:')
    print(listTokenFrequencies(getTokensFromList(indicesOfTrumpSubs, predicates)))
    # Print out the frequencies of tokens that occur as objects when Trump occurs in the subject
    print('Trump Object Frequencies:')
    print(listTokenFrequencies(getTokensFromList(indicesOfTrumpSubs, objects)))
    
    
    # Do the same thing for Clinton TODO: Extract this to a function
    clintonPreds = []
    clintonObjs = []
    print('\nClinton Triples:')
    for tripleIndex in indicesOfClintonSubs:
        print(subjects[tripleIndex], '|', predicates[tripleIndex], '|', objects[tripleIndex])
        clintonPreds.append(predicates[tripleIndex])
        clintonObjs.append(predicates[tripleIndex])

    # Print out the frequencies of tokens that occur as predicates when Clinton occurs in the subject
    print('Clinton Predicate Frequencies:')
    print(listTokenFrequencies(getTokensFromList(indicesOfClintonSubs, predicates)))
    # Print out the frequencies of tokens that occur as objects when Clinton occurs in the subject
    print('Clinton Object Frequencies:')
    print(listTokenFrequencies(getTokensFromList(indicesOfClintonSubs, objects)))

    # print("\nClinton Triples:")
    # for tripleIndex in indicesofClintonSubs:
    #     print(subjects[tripleIndex],'|', predicates[tripleIndex],'|', objects[tripleIndex])
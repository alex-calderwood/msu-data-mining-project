import xml.etree.ElementTree as ET

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


def occurances(list):
    trumps = []
    clintons = []

    for i in range(len(list)):
        text = list[i]
        if 'Trump' in text:
            trumps.append(i)
        elif 'Clinton' in text:
            clintons.append(i)

    print("Trump: ", len(trumps), "Clinton:", len(clintons))
    return trumps, clintons


if __name__ == '__main__':
    fileName = "test.xml"
    root = getXMLRoot(fileName)
    subjects, predicates, objects = getSPOTuples(root)

    print(subjects)
    occurances(subjects)

    print(predicates)
    occurances(predicates)

    print(objects)
    occurances(objects)






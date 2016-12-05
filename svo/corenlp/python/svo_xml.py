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


def occurances(entityList):
    trumpTripleIndices = []
    clintonTripleIndices = []

    for i in range(len(entityList)):
        text = entityList[i]
        if 'Trump' in text:
            trumpTripleIndices.append(i)
        elif 'Clinton' in text:
            clintonTripleIndices.append(i)

    print("Trump: ", len(trumpTripleIndices), "Clinton:", len(clintonTripleIndices))
    return trumpTripleIndices, clintonTripleIndices


if __name__ == '__main__':
    fileName = "test.xml"
    root = getXMLRoot(fileName)
    subjects, predicates, objects = getSPOTuples(root)

    print(subjects)
    subTrumps, subClintons = occurances(subjects)

    print(predicates)
    occurances(predicates)

    print(objects)
    occurances(objects)

    print('\nTrump Triples:')
    for tripleIndex in subTrumps:
        print(subjects[tripleIndex], predicates[tripleIndex], objects[tripleIndex])

    print("\nClinton Triples:")
    for tripleIndex in subClintons:
        print(subjects[tripleIndex], predicates[tripleIndex], objects[tripleIndex])

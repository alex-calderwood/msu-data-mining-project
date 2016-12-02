import xml.etree.ElementTree as ET

def getXMLRoot(xmlFileName):
    xmlTree = ET.parse(xmlFileName)
    xmlRoot = xmlTree.getroot()
    return xmlRoot

def getSPOTuples(xmlRoot):
    subjects = []
    predicates = []
    objects = []

    for node in xmlRoot:
        sentencesNode = node.findall('document.sentences')
        print(sentencesNode)

if __name__ == '__main__':
    fileName = "test.xml"
    root = getXMLRoot(fileName)
    for sentenceNode in root.find('document').find('sentences').findall('sentence'):
        for openie in sentenceNode.findall('openie'):
            for tripleNode in openie.findall('triple'):
                subjectNode = tripleNode.find('subject')
                predNode = tripleNode.find('relation')
                objectNode = tripleNode.find('object')

                print(subjectNode.find('text').text, '\t', predNode.find('text').text, '\t', objectNode.find('text').text)



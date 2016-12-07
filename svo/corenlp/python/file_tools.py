import xml.etree.ElementTree as ET
import os
import pickle


# Return the root of an xml file
def getXMLRoot(xmlFileName):
    xmlTree = ET.parse(xmlFileName)
    xmlRoot = xmlTree.getroot()
    return xmlRoot


# Return all non-hidden files in a directory, given a path to the directory from the script execution path
def getFilesFrom(pathTo):
    files = []
    for file in os.listdir(pathTo):
        # Ignore directories and hidden files
        if file[0] is '.':
            continue
        files.append(file)
    return files


# Not used currently, as it turned out to be very quick to run the xml reading code
def saveAsPickle(self, name, serializableData):
    with open(name + '.pickle', 'wb') as f:
        pickle.dump(serializableData, f)

        # If you need to save 2 things rather than one:
        # pickle.dump(self.data2, f)


def loadPickle(self, name):
    with open(name + '.pickle', 'rb') as f:
        return pickle.load(f)

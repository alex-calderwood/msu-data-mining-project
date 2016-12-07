import xml.etree.ElementTree as ET
import os
from nltk.stem.porter import PorterStemmer

import file_tools

pathToVerbnet = "../new_vn/"

debug = False

# Class to parse and store values of verbnet XML in dict form
class VerbNet:
    # Dictionary to hold verb meanings
    dictByVerb = {}

    # nltk stemmer
    ps = PorterStemmer()

    # Set of all verb roles
    allRoles = set()

    # Print function
    def print(self):
        print('dict:',  len(self.dictByVerb), self.dictByVerb)
        print('roles:', len(self.allRoles), self.allRoles)

    def readVerbnetFiles(self):
        for verbFile in os.listdir(pathToVerbnet):
            if(debug):
                print(verbFile)
            # Ignore directories and hidden files
            if verbFile[0] is '.':
                continue

            # Ignore non xml files
            if verbFile[-3:] != "xml":
                print('Ignoring', verbFile)
                continue

            # Get the verb semantic role from title
            verbRole = verbFile.split('-')[0]
            if debug:
                print('role:', verbRole)

            try:
                xmlRoot = file_tools.getXMLRoot(pathToVerbnet + verbFile)
                for node in xmlRoot.findall('MEMBERS/MEMBER'):

                    verbName = node.get('name')
                    verbStem = self.ps.stem(verbName)

                    if(debug):
                        print('\t' + verbStem)

                    if self.dictByVerb.get(verbStem) is None:
                        # Init a new list and add role to word
                        self.dictByVerb[verbStem] = [verbRole]
                    else:
                        # Add the role to the word
                        self.dictByVerb[verbStem].append(verbRole)

                    # Add the verbRole to a set of verb roles
                    self.allRoles.add(verbRole)

            except ET.ParseError:
                pass

        return self.dictByVerb

# Entry point if the file is run
if __name__ == '__main__':
    vn = VerbNet()
    vn.readVerbnetFiles()
    vn.print()
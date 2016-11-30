import Readability.DCReadability as DCR

textfile = open('Readability/test.txt', "r")

text = textfile.read()
DCR.grade(text)

textfile.close()
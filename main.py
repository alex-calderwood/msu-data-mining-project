from DCReadability import grade

textfile = open('test.txt', "r")

text = textfile.read()
grade(text)

textfile.close()
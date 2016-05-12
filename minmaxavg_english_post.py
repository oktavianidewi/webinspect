import numpy
import json
# open file
# filename = 'infotes.json'
filename = 'english_non_piBfoodgroup1.json'
# filename = 'english_non_piBconstitutionalpatriot1.json'
# filename = 'english_non_piBTEDTranslate1.json'
# filename = 'english_non_piBtraveladdiction1.json'
with open(filename) as file:
    data = json.load(file)

englishpostarr = []
totalpostarr = []
for itemperuser in data:
    if itemperuser['status'] == 'English' :
        englishpostarr.append(itemperuser['englishpost'])
        totalpostarr.append(itemperuser['totalpost'])

print "min post : ", min(englishpostarr)
print "avg post : ", round(numpy.mean(englishpostarr))
print "max post : ", max(totalpostarr)
import json
import nltk
import os
import string

# open file
# filename = 'infotes.json'
# filename = 'info_foodgroups.json'
filename = 'info_piBconstitutionalpatriot.json'
# filename = 'info_piBTEDTranslate.json'
# filename = 'info_piBtraveladdiction.json'
with open(filename) as file:
    data = json.load(file)

def writeToFile(data):
    # filename = "like_piBtraveladdiction.json"
    # filename = "like_piBTEDTranslate.json"
    filename = "like_piBconstitutionalpatriot.json"
    # filename = "like_piBfoodgroup.json"
    # filename = "like_infotes.json"
    # harus ada pengecekan fileexist atau ga
    isExist = os.path.isfile(filename)
    if isExist == True :
        # kalo file exist
        file = open(filename, "a")
    else :
        # kalo file not exist
        file = open(filename, "w+")
    file.write(json.dumps(data))
    file.close()
    return True

resultToWrite = []
x = []
hits = 0
numOfEnglishPostUser = 0
# get all timeline data
for userid in data:
    if 'like' in data[userid]:
        # if len(data[userid]['like']) > 0:
        likevalue = data[userid]['like']
        arrayLike = [ i for i in likevalue ]
        x += arrayLike

        tempList = []
        arrayUniqueCat = {}
        count = 0

        for i, e in enumerate(x):
            if e not in tempList :
                tempList.append(e)

        for item in tempList:
            count = 0
            for itemx in x:
                if item == itemx :
                    count += 1
            arrayUniqueCat[item] = count
resultToWrite = sorted(arrayUniqueCat.items(), key = lambda x:x[1], reverse=True)
writeToFile(resultToWrite)
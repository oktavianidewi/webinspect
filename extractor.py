import json
import nltk
import os
import string

ENGLISH_STOPWORDS = set(nltk.corpus.stopwords.words('english'))
NON_ENGLISH_STOPWORDS = set(nltk.corpus.stopwords.words()) - ENGLISH_STOPWORDS
STOPWORDS_DICT = {lang: set(nltk.corpus.stopwords.words(lang)) for lang in nltk.corpus.stopwords.fileids()}

def get_language(text):
    words = set(nltk.wordpunct_tokenize(text.lower()))
    return max(((lang, len(words & stopwords)) for lang, stopwords in STOPWORDS_DICT.items()), key = lambda x: x[1])[0]

def is_english(text):
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    text = text.lower()
    words = set(nltk.wordpunct_tokenize(text))
    stopwordsdetection = len(words & ENGLISH_STOPWORDS) > len(words & NON_ENGLISH_STOPWORDS)

    if not text:
        # print 'kosong'
        stopwordsdetection = False
    else:
        if not stopwordsdetection:
            textsplit = text.split(" ")
            # text_vocab = set(w.lower() for w in textsplit if w.lower().isalpha())
            text_vocab = set(" ".join("".join([" " if ch in string.punctuation else ch for ch in text.lower()]).split()).split())
            unusual = text_vocab.difference(english_vocab)
            usual = len(text_vocab)-len(unusual)
            if len(unusual) <= usual :
                stopwordsdetection = True
            else:
                stopwordsdetection = False
    # print stopwordsdetection, text
    return stopwordsdetection


# open file
# filename = 'infotes.json'
filename = 'info_foodgroups.json'
# filename = 'info_piBconstitutionalpatriot.json'
# filename = 'info_piBTEDTranslate.json'
# filename = 'info_piBtraveladdiction.json'
with open(filename) as file:
    data = json.load(file)

def countUserdID():
    if 'Store' in data :
        usercount = len(data)-1 # minus Store
    else:
        usercount = len(data)
    return usercount

# print countUserdID()

def getLike(*userID):
    if userID:
        likevalue = data[userID]['like']
        for i in likevalue:
            print i, '-> ',likevalue[i]
    else:
        for id in data:
            if id != 'Store':
                # print id
                # print data[id]['like']
                likevalue = data[id]['like']
                for i in likevalue:
                    print i, '-> ',likevalue[i]
    # return data

def getNoOfLike(userID):
    noOfLike = len(data[userID]['like'])
    return noOfLike

# print getNoOfLike('103421920043305')
# print getLike('103421920043305')
# print getLike()

def getAbout(*userID):
    # lengkapnya about di facebook itu apa aja? untuk menentukan nama kolom
    pass

def getTimeline(*userID):
    pass

english_non_details = {}
def detectLanguageFromUserPosts(userID):
    # checking english post atau bukan?
    userposts = data[userID]['timeline']
    numOfEnglishPost = 0
    for userpost in userposts:
        # index 12 is for posts
        stopwordsdetection = is_english(userpost[12])
        # print userpost[12]
        # print stopwordsdetection
        if stopwordsdetection:
            numOfEnglishPost += 1
    # print numOfEnglishPost, len(userposts)
    numOfUserPost = len(userposts)
    if numOfEnglishPost > 20:
        status = 'English'
    else:
        status = 'Non-English'
    return {"userid":userID,"status":status,"englishpost":numOfEnglishPost,"totalpost":numOfUserPost}
    # return status

def checkValidUser():
    pass

def writeToFile(data):
    # filename = "english_non_piBtraveladdiction.json"
    # filename = "english_non_piBTEDTranslate.json"
    # filename = "english_non_piBconstitutionalpatriot.json"
    filename = "english_non_piBfoodgroup1.json"
    # filename = "english_non_infotes.json"
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
numOfEnglishPostUser = 0
# get all timeline data
for userid in data:
    if userid != 'Store':
        print userid
        # english_non[userid] = detectLanguageFromUserPosts(userid)
        result = detectLanguageFromUserPosts(userid)
        if result['status'] == 'English':
            numOfEnglishPostUser += 1
    resultToWrite.append(result)
# writeToFile(resultToWrite)
print resultToWrite
print "numOfEnglishPostUser : ", numOfEnglishPostUser
import json
import nltk

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

    if not stopwordsdetection:
        # text = userpost[12].split(" ")
        textsplit = text.split(" ")
        text_vocab = set(w.lower() for w in textsplit if w.lower().isalpha())
        unusual = text_vocab.difference(english_vocab)
        # print text_vocab
        if len(unusual) < len(textsplit) :
            stopwordsdetection = True
        else:
            stopwordsdetection = False
    return stopwordsdetection


# open file
with open('infotes.json') as file:
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

# get all timeline data
"""
for userid in data:
    if userid != 'Store':
        print userid
        print data[userid]['timeline']
"""

def detectLanguageFromUserPosts(userID):
    # checking english post atau bukan?
    userposts = data[userID]['timeline']
    numOfEnglishPost = 0
    for userpost in userposts:
        # index 12 is for posts
        stopwordsdetection = is_english(userpost[12])
        if stopwordsdetection :
            numOfEnglishPost += 1
    if numOfEnglishPost > len(userposts)/2:
        status = 'English'
    else:
        status = 'Non-English'
    return status

def checkValidUser():
    pass


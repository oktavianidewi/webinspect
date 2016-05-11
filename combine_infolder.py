# -*- coding: utf-8 -*-
import os
import nltk
from bs4 import BeautifulSoup
import json
from textblob import TextBlob
import re
import time
from urllib import urlopen

def xtract_timeline():
    res = {}
    post_num = 0

    # Get the user url.
    try:
        url = soup.find(id = 'fb-timeline-cover-name').find_parent("a")["href"]
    except Exception, e:
        url = str(e).replace("'", "")

    # First we get the full name of the target.
    # Some posts in the timeline are not posted by the target user some we should get the name of the target to distinguish the posts.
    if soup.find(id = 'fb-timeline-cover-name'):
        user_name = soup.find(id = 'fb-timeline-cover-name').text
    else:
        # cannot find the target means this page is not available.
        print "Sorry, this page isn't available.\n"
        # continue
        pass

    # We get all the posts.
    the_posts = soup.find_all('div', attrs={'class':'userContentWrapper _5pcr'})

    # Analyse every post.
    for the_posts_num in range(the_posts.__len__()):
        # maybe this post is in the comment...

        # print the_posts[the_posts_num].find('div', attrs={'class': 'clearfix _5x46'})
        # the_posts[the_posts_num].find('div', attrs={'class': '_5x46'})

        if not the_posts[the_posts_num].find('div', attrs={'class': '_5x46'}):
            continue

        # list for the information of the post
        the_post_list = []
        the_post_list.append(url)
        the_post_list.append(user_name)

        # count the post.
        post_num += 1
        the_post_list.append(post_num)


        # head part. including title and time.
        the_post_head = the_posts[the_posts_num].find('div', attrs={'class': '_5x46'})

        # write part. including the text written by user.
        the_post_write = the_posts[the_posts_num].find('div', attrs={'class': 'userContent'})

        # media part. including what the user share, upload...
        the_post_media = the_posts[the_posts_num].find('div', attrs={'class': '_3x-2'})

        # comment part. including the likes, shares and comments information.
        # some post may not have comment part
        if len(the_posts[the_posts_num].find_all('form', attrs={'class': 'commentable_item'})) == 0:
            the_post_comment = ''
        else:
            # if the post is "shared a memory from", then it would have two "commentable_item".
            the_post_comment = the_posts[the_posts_num].find_all('form', attrs={'class': 'commentable_item'})[-1]


        # post title
        the_post_head_title = the_post_head.find('span', attrs={'class': 'fwn fcg'})
        the_post_head_title_text = the_post_head_title.text
        the_post_head_title_selforother = "self"
        the_post_head_title_names = the_post_head_title.find_all('a')
        if the_post_head_title_names[0].text not in user_name:
            the_post_head_title_selforother = "other"
        for the_post_head_title_name in the_post_head_title_names:
            the_post_head_title_text = the_post_head_title_text.replace(the_post_head_title_name.text, '')
        if the_post_head_title_text == "":
            the_post_head_title_text = "~"
        the_post_list.append(the_post_head_title_text)
        the_post_list.append(the_post_head_title_selforother)

        # BinSelforother
        if the_post_head_title_selforother == "self":
            the_post_list.append(1)
        else:
            the_post_list.append(0)

        # post time
        the_post_head_time = the_post_head.find('abbr', attrs={'class': '_5ptz'})
        try:
            the_post_head_time_text = str(the_post_head_time['title'])
        except Exception, e:
            the_post_head_time_text = str(e).replace("'", "")

        # weekday or weekend
        the_post_head_time_week = "Weekday"
        if ("Sunday" or "Saturday") in the_post_head_time_text:
            the_post_head_time_week = "Weekend"
        the_post_list.append(the_post_head_time_text)
        the_post_list.append(the_post_head_time_week)

        # BinWeekend
        if the_post_head_time_week == "Weekend":
            the_post_list.append(1)
        else:
            the_post_list.append(0)

        # post write text
        the_post_write_text = ""
        the_post_write_text_length = ''
        the_post_write_text_sentiment_polarity = ''
        the_post_write_text_sentiment_subjectivity = ''
        if the_post_write:
            the_post_write_text = the_post_write.text
            the_post_write_text_length = len(the_post_write_text)
            blob = TextBlob(the_post_write_text)
            the_post_write_text_sentiment = blob.sentiment
            the_post_write_text_sentiment_polarity = the_post_write_text_sentiment.polarity
            the_post_write_text_sentiment_subjectivity = the_post_write_text_sentiment.subjectivity
        if the_post_write:
            # BinPostText
            the_post_list.append(1)
            # BinEmoticon
            if the_post_write.find('span', attrs={'class': 'emoticon_text'}):
                the_post_list.append(1)
            else:
                the_post_list.append(0)
            # BinHashtag
            if the_post_write.find('span', attrs={'aria-label': 'hashtag'}):
                the_post_list.append(1)
            else:
                the_post_list.append(0)
        else:
            # if no text in post, then no emoticon and hashtag
            the_post_list.append(0)
            the_post_list.append(0)
            the_post_list.append(0)
        the_post_list.append(the_post_write_text)
        the_post_list.append(the_post_write_text_length)

        # BinPositive, BinNeutral, BinNegative
        if the_post_write_text_sentiment_polarity == '':
            the_post_list.append('')
            the_post_list.append('')
            the_post_list.append('')
        elif the_post_write_text_sentiment_polarity > 0:
            the_post_list.append(1)
            the_post_list.append(0)
            the_post_list.append(0)
        elif the_post_write_text_sentiment_polarity == 0:
            the_post_list.append(0)
            the_post_list.append(1)
            the_post_list.append(0)
        else:
            the_post_list.append(0)
            the_post_list.append(0)
            the_post_list.append(1)
        the_post_list.append(the_post_write_text_sentiment_polarity)
        the_post_list.append(the_post_write_text_sentiment_subjectivity)

        # check having facebook post text in the media or not
        the_post_media_share_post = the_post_media.find('div', attrs={'class': 'mtm _5pco'})
        the_post_media_share_post_text = ""

        # check having something not facebook like link and music or not
        the_post_media_share_link = the_post_media.find('div', attrs={'class': '_6m3'})
        the_post_media_share_link_title_text = ""
        the_post_media_share_link_content_text = ""
        the_post_media_share_link_source_text = ""

        if the_post_media_share_post:
            # is sharing text post (also maybe share something like memory from himself)
            # "share" may not in title
            the_post_media_share_post_text = the_post_media_share_post.text
        elif the_post_media_share_link:
            # is sharing something not facebook like link and music or not
            # this is the title
            the_post_media_share_link_title = the_post_media_share_link.find('div', attrs={'class': 'mbs _6m6'})
            # some class may be something like "_5wj- mbs _6m6". maybe using "_6m6" but I am not going to take the risk.
            if the_post_media_share_link_title:
                the_post_media_share_link_title_text = the_post_media_share_link_title.text
            else:
                the_post_media_share_link_title = the_post_media_share_link.find('div', attrs={'class': '_6m6'})
                the_post_media_share_link_title_text = the_post_media_share_link_title.text
            # this is the content. for music sometimes may no content.
            the_post_media_share_link_content = the_post_media_share_link.find('div', attrs={'class': '_6m7'})
            the_post_media_share_link_content_text = ""
            # for music sometimes may no content.
            if the_post_media_share_link_content:
                the_post_media_share_link_content_text = the_post_media_share_link_content.text
            # this is the source URL. sometimes may also write '|By ' to show who report. we filter it.
            the_post_media_share_link_source = the_post_media_share_link.find('div', attrs={'class': '_59tj'})
            the_post_media_share_link_source_text = ""
            # some share may not have source
            if the_post_media_share_link_source:
                if the_post_media_share_link_source.text.find('|By ') != -1:
                    the_post_media_share_link_source_text = the_post_media_share_link_source.text[: the_post_media_share_link_source.text.find('|By ')]
                else:
                    the_post_media_share_link_source_text = the_post_media_share_link_source.text

        if the_post_media_share_post:
            # BinShareFacebook
            the_post_list.append(1)
            the_post_list.append(the_post_media_share_post_text)
            blob = TextBlob(the_post_media_share_post_text)
            the_post_list.append(blob.polarity)
            the_post_list.append(blob.subjectivity)
        else:
            the_post_list.append(0)
            the_post_list.append("")
            the_post_list.append('')
            the_post_list.append('')
        if the_post_media_share_link:
            # BinShareLink
            the_post_list.append(1)
            the_post_list.append(the_post_media_share_link_title_text)
            the_post_list.append(the_post_media_share_link_content_text)
            the_post_list.append(the_post_media_share_link_source_text)
            blob = TextBlob(the_post_media_share_link_title_text)
            the_post_list.append(blob.polarity)
            the_post_list.append(blob.subjectivity)
        else:
            the_post_list.append(0)
            the_post_list.append("")
            the_post_list.append("")
            the_post_list.append("")
            the_post_list.append('')
            the_post_list.append('')

        # BinURL - check write part and media part.
        if (("http://" or "www.") in the_post_write_text) or the_post_media_share_link:
            the_post_list.append(1)
        else:
            the_post_list.append(0)

        # BinSharing
        if "shared" in the_post_head_title_text:
            the_post_list.append(1)
        elif the_post_media_share_post:
            the_post_list.append(1)
        else:
            the_post_list.append(0)

        # if comment part not exists, add nothing about the comment to the post information. stop adding.
        if the_post_comment != '':
            # likes count
            the_post_comment_likes = the_post_comment.find('div', attrs={'class': 'UFILikeSentenceText'})
            the_post_comment_likes_count = 0
            if the_post_comment_likes:
                if 'likes' in the_post_comment_likes.text:
                    the_post_comment_likes_count = 1
                else:
                    the_post_comment_likes_count = the_post_comment_likes.text[: the_post_comment_likes.text.find("people")-1]
            the_post_list.append(the_post_comment_likes_count)
            # share count
            the_post_comment_shares = the_post_comment.find('div', attrs={'class': 'UFIRow UFIShareRow'})
            the_post_comment_shares_count = 0
            if the_post_comment_shares:
                if 'shares' in the_post_comment_shares.text:
                    the_post_comment_shares_count = the_post_comment_shares.text[: the_post_comment_shares.text.find("shares")-1]
                else:
                    the_post_comment_shares_count = 1
            the_post_list.append(the_post_comment_shares_count)
            # comment count
            the_post_comment_comments_more = the_post_comment.find('a', attrs={'class': 'UFIPagerLink'})
            the_post_comment_comments_list = the_post_comment.find_all('div', attrs={'aria-label': 'Comment'})
            the_post_comment_comments_count = 0
            if the_post_comment_comments_more:
                if 'previous' not in the_post_comment_comments_more.text:
                    if 'all' not in the_post_comment_comments_more.text:
                        # "UFIPagerLink" may find the "View more replies" in the comments
                        if "repl" not in the_post_comment_comments_more.text:
                            the_post_comment_comments_count = the_post_comment_comments_more.text[5:the_post_comment_comments_more.text.find("more")-1]
                            # print the_post_comment_comments_count.split(' ')[0]
                            # ada data yang valuenya '1 comme'
                            the_post_comment_comments_count = int(the_post_comment_comments_count.split(' ')[0]) + 4
                    else:
                        the_post_comment_comments_count = the_post_comment_comments_more.text[9:the_post_comment_comments_more.text.find("comment")-1]
                else:
                    the_post_comment_comments_more = the_post_comment.find('span', attrs={'class': 'fcg UFIPagerCount'})
                    the_post_comment_comments_count = \
                        the_post_comment_comments_more.text[the_post_comment_comments_more.text.find("of")+3:]
            elif the_post_comment_comments_list:
                the_post_comment_comments_count = len(the_post_comment_comments_list)
            the_post_list.append(the_post_comment_comments_count)
            # comment content
            # the_post_comment_comments_list_contents storage the list of the top (at most 4) comments information
            the_post_comment_comments_list_contents = []
            # browse every comment
            if the_post_comment_comments_list:
                for the_post_comment_comments_list_comment in the_post_comment_comments_list:
                    # the_post_comment_comments_list_content storage a list of information of this comment.
                    # there are: commented by self or other, text, length, polarity, subjectivity.
                    the_post_comment_comments_list_content = []
                    # comment text
                    the_post_comment_comments_list_comment_text = \
                        the_post_comment_comments_list_comment.find('span', attrs={'class': 'UFICommentBody'}).text
                    the_post_comment_comments_list_comment_name = \
                        the_post_comment_comments_list_comment.find('a', attrs={'class': 'UFICommentActorName'}).text
                    # commented by self or other
                    the_post_comment_comments_list_comment_selforother = "other"
                    if the_post_comment_comments_list_comment_name in user_name:
                        the_post_comment_comments_list_comment_selforother = "self"
                    # comment text length
                    the_post_comment_comments_list_comment_text_length = len(the_post_comment_comments_list_comment_text)
                    blob = TextBlob(the_post_comment_comments_list_comment_text)
                    the_post_comment_comments_list_comment_text_sentiment = blob.sentiment
                    # comment text polarity
                    the_post_comment_comments_list_comment_text_sentiment_polarity \
                        = the_post_comment_comments_list_comment_text_sentiment.polarity
                    # comment text subjectivity
                    the_post_comment_comments_list_comment_text_sentiment_subjectivity \
                        = the_post_comment_comments_list_comment_text_sentiment.subjectivity
                    # save the information of the comment to the list
                    the_post_comment_comments_list_content.append(the_post_comment_comments_list_comment_selforother)
                    # BinTopCommentSelforother
                    if the_post_comment_comments_list_comment_selforother == "self":
                        the_post_comment_comments_list_content.append(1)
                    else:
                        the_post_comment_comments_list_content.append(0)
                    the_post_comment_comments_list_content.append(the_post_comment_comments_list_comment_text)
                    the_post_comment_comments_list_content.append(the_post_comment_comments_list_comment_text_length)
                    the_post_comment_comments_list_content.append(the_post_comment_comments_list_comment_text_sentiment.polarity)
                    the_post_comment_comments_list_content.append(the_post_comment_comments_list_comment_text_sentiment.subjectivity)
                    # save the information list of the comment to the comments list
                    the_post_comment_comments_list_contents.append(the_post_comment_comments_list_content)
            # Top4 comments
            temp_comment_count = 4
            if the_post_comment_comments_list_contents:
                for the_post_comment_comments_list_content in the_post_comment_comments_list_contents:
                    temp_comment_count -= 1
                    for the_post_comment_comments_list in the_post_comment_comments_list_content:
                        the_post_list.append(the_post_comment_comments_list)
            if temp_comment_count != 0:
                for i in range(temp_comment_count):
                    for j in range(6):
                        the_post_list.append('')

        all_post_list.append(the_post_list)

    # res['timeline'] = all_post_list
    return all_post_list


def xtract_like():
    likes = {}
    res = {}
    try:
        ullikes = soup.find_all(attrs={'class':'uiList _4-sn _5k35 _620 _509- _4ki'})
        # print likes
        for indexsub in range(0, len(ullikes)):
            itemsliked = ullikes[indexsub].find_all(attrs={'class':'fsl fwb fcb'})
            subcategoryitemsliked = ullikes[indexsub].find_all(attrs={'class':'fsm fwn fcg'})
            for index in range(0, len(itemsliked) ) :
                likes[subcategoryitemsliked[index].text] = itemsliked[index].text
    except Exception, e:
        likes['error'] = str(e).replace("'", "")

    # res['likes'] = likes
    return likes

def xtract_about():
    # extract username
    identity = {}
    uname = {}
    about = {}
    res = {}

    try:
        identity[0] = soup.find(attrs={'class':'bq'}).span.strong.text
        # extract username
        uname['username'] = identity[0]

        try:
            y = soup.find('span', attrs={'class':'bu bv'}).find_all('div', attrs={'class':'bl bw'})
            for c in range(0, len(y)):
                identity[c+1] = y[c].span.text
            # print identity
        except AttributeError:
            pass

        # extract ABOUT
        # kemungkinan 1: content-not-available
        # kemungkinan 2: data ditemukan
        contents = soup.find(attrs={'class':'bg bh'}).find_all(with_id)

        for idx in range(0, len(contents)):
            # kalau len == 1, value nya ditampilkan diatas
            # print len(contents[idx].find_all('table'))

            if len(contents[idx].find_all('table')) == 1:
                if len(identity) > 1:
                    about[contents[idx].find_all('table')[0].text] = identity[idx+1]
            else:
                sub = contents[idx].find_all('table')
                for idxsub in range(0, len(sub)):
                    isiidxsub = sub[idxsub].find_all('div')
                    # print isiidxsub
                    lenidxsub = len(sub[idxsub].find_all('div'))

                    # jika index ke-1 tidak kosong
                    if isiidxsub[1].text:
                        for idxsubsub in range(0, lenidxsub):
                            if idxsubsub == 0:
                                about[isiidxsub[0].text] = isiidxsub[1].text
    except Exception, e:
        # about['error'] = e
        about['error'] = str(e).replace("'", "")

    # res['about'] = about
    return about

def writeToJsonFile(data, jsonfile):
    with open(jsonfile, 'w') as file:
        file.write( json.dumps(data) )
        file.close()
    return True

if __name__ == '__main__':

    # for root, dirs, files in os.walk("C:/Users/admin/Desktop/python/facebook/catch posting type/combine 16.4.24/html_source"):
    # for root, dirs, files in os.walk("D:/githubrepository/webscrapper/webinspect/piBTEDTranslate"):
    def with_id(tag):
        return tag.has_attr('id')

    def with_class(tag):
        return tag.has_attr('class')

    # for root, dirs, files in os.walk("D:\githubrepository\webscrapper\webinspect/try_inspect/4340266040557"):
    directory = "foodgroups"
    # directory = "try_inspect"
    user_num = 0
    infoperuser = {}
    alluserinfo = []

    for root, dirs, files in os.walk(directory):

        # save the all posts
        all_post_list = []
        # Browse the html files
        all = {}
        file = {}
        for dir in dirs:
            file[''+dir+''] = {}
            file['a'] = {}

        # print dirs[user_num]

        for name in files:
            if name != '.DS_Store':
                print 'name : ', name

                # post number for every user
                post_num = 0

                # read the file
                file_path_raw = root + '/' + name
                file_path = file_path_raw.replace('\\', '/')
                user_file = open(file_path, 'r')
                user_lines = user_file.read()

                soup = BeautifulSoup(user_lines, "html.parser")

                # extract likes
                if 'like' in file_path:
                    likeres = xtract_like()
                    print likeres
                    file['like'] = likeres
                elif 'about' in file_path:
                    # extract about
                    aboutres = xtract_about()
                    print aboutres
                    file['about'] = aboutres
                elif 'timeline' in file_path:
                    # extract timeline
                    timelineres = xtract_timeline()
                    print timelineres
                    file['timeline'] = timelineres
            userid = str(name.split('_')[1].split('.')[0])
            infoperuser[userid] = file
    print infoperuser
    # writeToJsonFile(infoperuser, "infotes.json")
    writeToJsonFile(infoperuser, "info_foodgroups.json")

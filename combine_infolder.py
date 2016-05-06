# -*- coding: utf-8 -*-
import os
import nltk
from bs4 import BeautifulSoup
import xlwt
from textblob import TextBlob
import re
import time

if __name__ == '__main__':

    # for root, dirs, files in os.walk("C:/Users/admin/Desktop/python/facebook/catch posting type/combine 16.4.24/html_source"):
    # for root, dirs, files in os.walk("D:/githubrepository/webscrapper/webinspect/piBTEDTranslate"):
    def with_id(tag):
        return tag.has_attr('id')

    def with_class(tag):
        return tag.has_attr('class')

    # 4651658826994
    # 4340266040557
    for root, dirs, files in os.walk("D:\githubrepository\webscrapper\webinspect/try_inspect/4340266040557"):
        user_num = 0
        # save the all posts
        all_post_list = []
        # Browse the html files
        for name in files:
            # post number for every user
            post_num = 0

            # Count the user number.
            user_num += 1

            # read the file
            file_path_raw = root + '/' + name
            print"-----------------------------------------------"
            file_path = file_path_raw.replace('\\', '/')
            user_file = open(file_path, 'r')
            user_lines = user_file.read()
            soup = BeautifulSoup(user_lines, "html.parser")

            # extract username

            identity = {}
            uname = {}
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
            about = {}
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

            print uname
            print about

            # extract likes
            # extract timeline
            """
            for idx in range(0, len(contents)):
                print len(contents[idx].find_all('table'))
                print contents[idx].find_all('table')
            """
                # print contents[idx].find_all('table')

                # print contents[idx].find('span', attrs={'class':'cs cq ct'}).text
                # print contents[idx].find('div', attrs={'class': 'cv'}).text
                # about[ contents[idx].find('span', attrs={'class':'cs cq ct'}).text ] = contents[idx].find('div', attrs={'class': 'cv'}).text

                # print uname
                # print about
                # quit()

                # extract timeline
                # extract like

                # url = soup.find(id = 'fb-timeline-cover-name').find_parent("a")["href"]

                # print(len(all_post_list))
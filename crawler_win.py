import os
import sys
import socket
import os.path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import datetime
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
"""
"""

# import BeautifulSoup
# import json
# from selenium.webdriver.common.action_chains import ActionChains
# import random

def directoryexist(userid):
    # create folder
    directory = userid
    if not os.path.exists(directory):
        os.makedirs(directory)
    directoryIsExist = True
    return directoryIsExist

def savepage(type, userid):
    # directory is based on userid
    directory = userid.rstrip('\n')
    # checking directory
    checking = directoryexist(directory)
    page_html = driver.page_source
    page_html_file = open(directory+'/'+type+'_'+userid+'.html', 'w')
    page_html_file.write(page_html)
    page_html_file.close()

def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def scrollLikePage(current_url, userid):
    # scroll until got 100 top-likes
    likes_url = current_url+'/likes'
    driver.get(likes_url)
    time.sleep(1)
    current_url_after_redirect = driver.current_url

    if current_url_after_redirect == likes_url :
        background = driver.find_element_by_css_selector("body")
        for i in range(1, 20):
            time.sleep(0.7)
            background.send_keys(Keys.SPACE)
    savepage('likes', userid)
    # rlog(userid, likes_url)

def scrollTimelinePage(current_url, userid):
    background = driver.find_element_by_css_selector("body")
    # Better to stop here. Or it may have exception at background.send_keys(Keys.SPACE).
    # time.sleep(3)

    # Prevent invalid page.
    try:
        driver.find_element_by_id('fb-timeline-cover-name')
    except Exception, e:
        # save these URLs
        rlog('timeline','invalid page : %s ' %(e),0, userid)

    try:
        # set default scrolllimit
        scrolllimit = 4
        stop = False
        yearlimit = 2015
        startTag = 0
        recordOfTagNum = []
        sleeptime = 3
        constantlength = False
        while (stop == False and constantlength == False):
            # do scrolling
            for i in range(1, scrolllimit):
                background.send_keys(Keys.SPACE)
            time.sleep(sleeptime)

            # find elements by class
            tag = driver.find_elements_by_css_selector('._5ptz')

            # antisipasi kalo user punya banyak post
            # antisipasi kalo user punya post banyak
            if tag.__len__() > 350 :
                stop = True
            else:
                stop = False

            # antisipasi post user sedikit dan tahunnya > yearlimit
            countOfMax = [a for a in recordOfTagNum if a == max(recordOfTagNum)]
            recordOfTagNum.append(tag.__len__())
            if len(recordOfTagNum) > 5:
                print recordOfTagNum
                # compare
                # True and True
                if (recordOfTagNum[0] == recordOfTagNum[recordOfTagNum.index(max(recordOfTagNum))]) and (len(countOfMax) > 10) :
                    constantlength = True
                elif (recordOfTagNum[0] != recordOfTagNum[recordOfTagNum.index(max(recordOfTagNum))]) and (len(countOfMax) > 10) :
                    constantlength = True
                elif (recordOfTagNum[0] == recordOfTagNum[recordOfTagNum.index(max(recordOfTagNum))]) and (len(countOfMax) < 10) :
                    constantlength = True
                else:
                    constantlength = False

            # antisipasi kalo loading tiba2 berhenti

            # nilai start dinamis
            for x in range(startTag, tag.__len__()):
                postyear = (tag[x].get_attribute("title")).split(" ")
                tahun = int(postyear[3])
                print tag[x].get_attribute("title")
                print x
                if yearlimit <= tahun:
                    stop = False
                else:
                    stop = True
                startTag = x+1
        savepage('timeline', userid)
        """
        try:
            savepage('timeline', userid)
        except Exception, e:
            rlog('timeline','keterangan error: %s' %(e),startrow, userid)
        """
    except TimeoutException:
        rlog('timeline','keterangan timeout : %s' %(e),startrow, userid)
    # rlog(userid, url)

def scrollAboutPage(current_url, userid):
    # browse ABOUT page
    username = current_url.split('/')[3]
    about_url = 'https://m.facebook.com/'+username+'/about'
    # open page based on url
    driver.get(about_url)
    # save webpage
    savepage("about", userid)

# rlog('timeline','success',startrow, userid)
def rlog(type, status, i, userid):
    date = time.strftime('%Y%m%d',time.localtime(time.time()))
    # Record the start time.
    starttime = datetime.datetime.now()
    filename = "log_"+date+".txt"
    teks = "%s,%s,%s,%s,%s \n" % (type, status, starttime, i, userid)

    # harus ada pengecekan fileexist atau ga
    isExist = os.path.isfile(filename)
    if isExist == True :
        # kalo file exist
        file = open(filename, "a")
    else :
        # kalo file not exist
        file = open(filename, "w+")
    file.write(teks)
    file.close()
    return True

def lastCheckedNum(logfilename):
    # menentukan startrow dari file log
    checkeduser = []
    with open(logfilename, 'r') as row:
        x = row.readlines()
        if len(x) > 1:
            for baris in x:
                row = baris.split(',')[3]
                if row not in checkeduser:
                    checkeduser.append(row)
            start = max(checkeduser)
        else:
            start = 1
    return start

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # get userid from .csv file
    urls = []
    # samples = open('../FBCrawl/piBfoodgroups.csv','r')
    # samples = open('../FBCrawl/piBTEDtranslate.csv','r')
    samples = open('D:\githubrepository\FBCrawl\piBTEDTranslate.csv','r')
    readfile = samples.readlines()
    baseurl = 'www.facebook.com/'

    # filter unique user
    # startrow = lastCheckedNum('log_20160501.txt')
    # startrow = lastCheckedNum('log_20160501.txt')
    startrow = 1
    endrow = readfile.__len__()
    for idx in range(startrow, endrow):
        getuserid = readfile[idx]
        urls.append(getuserid)

    print "unique user : ", len(urls)

    # driver init
    driver = webdriver.Firefox()
    # Set the timeout for the driver and socket.
    driver.set_page_load_timeout(20)
    # socket.setdefaulttimeout(10)

    # First, login.
    driver.get("https://www.facebook.com/login.php")
    # time.sleep(3)
    driver.find_element_by_id("email").clear()
    driver.find_element_by_id("email").send_keys("dev.oktaviani.dewi@gmail.com")
    driver.find_element_by_id("pass").clear()
    driver.find_element_by_id("pass").send_keys("zGq-8ev-Z7e-vYh")
    driver.find_element_by_id("loginbutton").click()
    # Better wait for several seconds.
    # time.sleep(3)

    # Maybe the login failed. It may turn to the login page again.
    # you may need to load again.
    if 'login' in driver.current_url:
        driver.close()

    # visit the url based on urls
    for useridraw in urls:
        time.sleep(1)

        userid = useridraw.rstrip('\n')
        url = baseurl+userid
        print(url)
        # you should know how long you scroll in this timeline - for set the timeout
        # Print the start time.
        print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))
        # Wait 3 seconds for the browser loading the Webpage.
        # time.sleep(3)

        driver.get(url)
        # cari scc selector yg ada di halaman likes. supaya bisa discroll
        # tabs = ['timeline', 'likes', 'about']
        current_url = driver.current_url

        try:
            scrollTimelinePage(current_url, userid)
            rlog('timeline','success',idx, userid)
        except Exception, e:
            rlog('timeline','failed : %s' %(e),idx, userid)

        try:
            scrollLikePage(current_url, userid)
            rlog('like','success',idx, userid)
        except Exception, e:
            rlog('like','failed : %s' %(e),idx, userid)

        try:
            scrollAboutPage(current_url, userid)
            rlog('about','success',idx, userid)
        except Exception, e:
            rlog('about','failed : %s' %(e),idx, userid)
            continue

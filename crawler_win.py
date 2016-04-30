import os
import sys
import socket
import os.path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import datetime
import time

"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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
    directory = userid

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
    # browse the TIMELINE based on scrolllimit
    driver.get(url)
    background = driver.find_element_by_css_selector("body")
    # Better to stop here. Or it may have exception at background.send_keys(Keys.SPACE).
    # time.sleep(3)

    # Prevent invalid page.
    try:
        driver.find_element_by_id('fb-timeline-cover-name')
    except Exception, e:
        # save these URLs
        rlog('timeline',e,startrow, userid)

    try:
        # set default scrolllimit
        scrolllimit = 4
        stop = False
        yearlimit = 2015
        # delay = 100
        sleeptime = 3
        while stop == False:
            # do scrolling
            for i in range(1, scrolllimit):
                background.send_keys(Keys.SPACE)
            time.sleep(sleeptime)
            """
            <img width="16" height="11" alt="" src="https://static.xx.fbcdn.net/rsrc.php/v2/yb/r/GsNJNwuI-UM.gif" class="ptl loadingIndicator img">
            """
            # try:

            # find elements by class
            tag = driver.find_elements_by_css_selector('._5ptz')
            for x in range(0, tag.__len__()):
                # pengen tau apa aja isinya abbr
                print tag[x].get_attribute("title")

                postyear = (tag[x].get_attribute("title")).split(" ")
                tahun = int(postyear[3])
                print tag[x].get_attribute("title")
                print yearlimit <= tahun
                if yearlimit <= tahun:
                    stop = False
                    # sleeptime += 2
                else:
                    stop = True
            savepage('timeline', userid)
    except socket.timeout:
        rlog('timeline','socket timeout',startrow, userid)


    # rlog(userid, url)

def scrollAboutPage(current_url, userid):
    # browse ABOUT page
    username = current_url.split('/')[3]
    about_url = 'https://m.facebook.com/'+username+'/about'
    # open page based on url
    driver.get(about_url)
    # save webpage
    savepage("about", userid)

    """
    about = ['education', 'overview', 'living', 'contact-info', 'relationship', 'bio', 'year-overviews']
    for sectionname in about:
        about_url = current_url+'/about?section=%s&pnref=about' %(sectionname)
        # open page based on url
        driver.get(about_url)
        # save webpage
        savepage(sectionname, userid)
        # rlog(userid, about_url)
    """
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

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # get userid from .csv file
    urls = []
    samples = open('../FBCrawl/piTEDtranslate.csv','r')
    # samples = open('D:\githubrepository\FBCrawl\pitraveladdiction.csv','r')
    readfile = samples.readlines()
    baseurl = 'www.facebook.com/'

    # filter unique user
    startrow = 8+5+1+1+1+3+1
    endrow = startrow + 2
    # endrow = readfile.__len__()
    for idx in range(startrow, endrow):
        # urls.append(baseurl+readfile[idx].split(',')[1])
        getuserid = readfile[idx].split(',')[1]

        if getuserid not in urls:
            urls.append(getuserid)

    print "unique user : ", len(urls)

    # driver init
    driver = webdriver.Firefox()
    # Set the timeout for the driver and socket.
    # driver.set_page_load_timeout(30)
    socket.setdefaulttimeout(20)

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
    for userid in urls:
        time.sleep(1)

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
            rlog('timeline','success',startrow, userid)
        except Exception, e:
            rlog('timeline','failed',startrow, userid)

        try:
            scrollLikePage(current_url, userid)
            rlog('like','success',startrow, userid)
        except Exception, e:
            rlog('like','failed',startrow, userid)

        try:
            scrollAboutPage(current_url, userid)
            rlog('about','success',startrow, userid)
        except Exception, e:
            rlog('about','failed',startrow, userid)
            continue

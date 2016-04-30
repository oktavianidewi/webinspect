import os
import sys
import socket
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import datetime
import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
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

    """
        # limit
        # kalo g nemu yg tahun 2014 gimana?
        <div class="_4-u2 _2uo1 _3-95 _4-u8" id="u_jsonp_3_0_yearoverview" data-referrer="u_jsonp_3_0_yearoverview"><div class="_2pi6 _52jv"><i class="_3-94 img sp_GPqZJ_sO3wF sx_412bb0"></i><div class="_50f9 _50f6">Posts from 2015</div></div></div>
        <div class="_4-u2 _2uo1 _3-95 _4-u8" id="u_jsonp_4_0_yearoverview" data-referrer="u_jsonp_4_0_yearoverview"><div class="_2pi6 _52jv"><i class="_3-94 img sp_GPqZJ_sO3wF sx_412bb0"></i><div class="_50f9 _50f6">Posts from 2014</div></div></div>
        _4-u2 _2uo1 _3-95 _4-u8
        //*[@id="u_jsonp_9_0_yearoverview"]/div/div -> tahun 2012
        //*[@id="u_jsonp_8_0_yearoverview"]/div/div

    """

    # Prevent invalid page.
    try:
        driver.find_element_by_id('fb-timeline-cover-name')
    except Exception, e:
        # save these URLs
        failed_file = open('failed_page.txt', 'a')
        failed_file.write(url)
        failed_file.write(str(Exception)+': '+str(e))
        failed_file.close()
    try:
        # set default scrolllimit
        scrolllimit = 1
        stop = False
        yearlimit = 2015

        while stop == False:
            for i in range(1, scrolllimit):
                background.send_keys(Keys.SPACE)
                time.sleep(10)
            # tag = driver.find_elements_by_tag_name('abbr')
            # tag = driver.find_elements_by_xpath('//*[@id="u_0_1b"]/div[2]/div[1]/div[3]/div/div/div[2]/div/div/div[2]/div')
            tag = driver.find_elements_by_css_selector('#timestampContent')
            print tag.__len__()

            """
            <abbr title="Sunday, November 22, 2015 at 5:21pm" data-utime="1448241677" data-shorten="1" class="_5ptz"><span id="js_2" class="timestampContent">November 22, 2015</span></abbr>
            another abbr
            <abbr data-shorten="true" data-utime="1448212893" title="Monday, November 23, 2015 at 2:21am" class="livetimestamp">November 23, 2015 at 2:21am</abbr>
            <abbr data-shorten="true" data-utime="1448216339" title="Monday, November 23, 2015 at 3:18am" class="livetimestamp">November 23, 2015 at 3:18am</abbr>

            """
            for x in range(0, tag.__len__()):
                # pengen tau apa aja isinya abbr
                print tag[x].get_attribute("title")

                postyear = (tag[x].get_attribute("title")).split(" ")
                if len(postyear) > 4:
                    tahun = int(postyear[3])
                # print postyear[3]
                # quit()
                print yearlimit <= tahun
                if yearlimit <= tahun:
                    # print "lanjut"
                    stop = False
                    scrolllimit += 1
                else:
                    # print "stop"
                    stop = True

    except socket.timeout:
        print "Exception Timeout: " + url
        socket_timeout_file = open('socket_timeout.txt', 'a')
        socket_timeout_file.write(url)
        socket_timeout_file.close()

    savepage('timeline', userid)
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

def rlog(i, userid):
    date = time.strftime('%Y%m%d',time.localtime(time.time()))
    # Record the start time.
    starttime = datetime.datetime.now()
    filename = "log_"+date+".txt"
    # getfilename = fileexist(filename)
    teks = "%s,%s,%s" % (i,userid,time)
    # teks = str(i)+','+str(userid)+','str(time)
    file = open(filename, "r+")
    file.write(teks)
    file.close()
    return True

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # get userid from .csv file
    urls = []
    samples = open('../FBCrawl/piTEDtranslate.csv','r')
    # samples = open('D:\githubrepository\FBCrawl\piTEDtranslate.csv','r')
    readfile = samples.readlines()
    baseurl = 'www.facebook.com/'

    # filter unique user
    startrow = 22+1+1+1+1+1+1+1
    # endrow = readfile.__len__()
    endrow = startrow+1
    for idx in range(startrow, endrow):
        # urls.append(baseurl+readfile[idx].split(',')[1])
        getuserid = readfile[idx].split(',')[1]

        if getuserid not in urls:
            urls.append(getuserid)

    print "unique user : ", len(urls)

    # driver init
    driver = webdriver.Firefox()
    # Set the timeout for the driver and socket.
    driver.set_page_load_timeout(30)
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
        time.sleep(3)
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

        scrollTimelinePage(current_url, userid)
        scrollLikePage(current_url, userid)
        scrollAboutPage(current_url, userid)
        rlog(startrow, userid, )
        continue
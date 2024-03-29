import os
import sys
import socket
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import time

# from selenium.webdriver.common.by import By
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

"""
def fileexist(filename):
    idx = 1
    if not os.path.isfile(filename):
        # buat file dg nama filename tsb
        os.makedirs(filename)
    else:
        # rename file dg nama filename tsb + index
    return
"""
def savepage(type, userid):
    # directory is based on userid
    directory = userid

    # checking directory
    checking = directoryexist(directory)

    page_html = driver.page_source
    page_html_file = open(directory+'/'+type+'_'+userid+'.html', 'w')
    page_html_file.write(page_html)
    page_html_file.close()

def scrollLikePage(current_url, userid):
    # scroll until got 100 top-likes
    likes_url = current_url+'/likes'
    driver.get(likes_url)
    background = driver.find_element_by_css_selector("body")
    for i in range(1, 20):
        time.sleep(0.1)
        background.send_keys(Keys.SPACE)
    savepage('likes', userid)
    # rlog(userid, likes_url)

def scrollTimelinePage(current_url, userid):
    # browse the TIMELINE based on scrolllimit
    # Go to the target's timeline Webpage.
    driver.get(url)
    # For scroll the page: send_keys(Keys.SPACE)
    background = driver.find_element_by_css_selector("body")
    # Better to stop here. Or it may have exception at background.send_keys(Keys.SPACE).
    # time.sleep(3)

    # Prevent invalid page.
    try:
        driver.find_element_by_id('fb-timeline-cover-name')
    except Exception, e:
        # save these URLs
        failed_file = open('failed_page.txt', 'a')
        failed_file.write(url)
        failed_file.write(str(Exception)+': '+str(e))
        failed_file.close()

    found = False
    try:
        # set default scrolllimit
        scrolllimit = 10
        yearlimit = '2015'

        while found == False:
            for i in range(1, scrolllimit):
                time.sleep(0.1)
                background.send_keys(Keys.SPACE)

            """
            # limit
            <div class="_4-u2 _2uo1 _3-95 _4-u8" id="u_jsonp_3_0_yearoverview" data-referrer="u_jsonp_3_0_yearoverview"><div class="_2pi6 _52jv"><i class="_3-94 img sp_GPqZJ_sO3wF sx_412bb0"></i><div class="_50f9 _50f6">Posts from 2015</div></div></div>
            <div class="_4-u2 _2uo1 _3-95 _4-u8" id="u_jsonp_4_0_yearoverview" data-referrer="u_jsonp_4_0_yearoverview"><div class="_2pi6 _52jv"><i class="_3-94 img sp_GPqZJ_sO3wF sx_412bb0"></i><div class="_50f9 _50f6">Posts from 2014</div></div></div>
            """
            # tag = driver.find_elements_by_tag_name('abbr')
            tag = driver.find_elements_by_xpath('//*[@id="u_jsonp_4_0_yearoverview"]/div/div')
            print tag.__len__()
            limit = tag.__len__()
            print "continue"
            for x in range(0, limit):
                title = tag[x].get_attribute("title")
                if yearlimit in title :
                    found = True
                    limit = x
                    scrolllimit = 0
                else:
                    found = False
                    limit = tag.__len__()
                    scrolllimit += 1

                print title
                print found

    except socket.timeout:
        print "Exception Timeout: " + url
        socket_timeout_file = open('socket_timeout.txt', 'a')
        socket_timeout_file.write(url)
        socket_timeout_file.close()

    savepage('timeline', userid)
    # rlog(userid, url)

def scrollAboutPage(current_url, userid):
    # browse ABOUT page
    # driver.find_element_by_xpath('//*[@id="u_0_r"]/div/a[2]').click()
    # likes_url = current_url+'/about'
    # ABOUT
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

def rlog(userid, link):
    i = 1
    date = time.strftime('%Y%m%d',time.localtime(time.time()))
    # Record the start time.
    starttime = datetime.datetime.now()
    filename = "log_"+date
    # getfilename = fileexist(filename)
    file = open(filename, "a")
    file.write(userid+','+link+','+time)
    file.close()
    return True

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    # get userid from .csv file
    urls = []
    samples = open('../FBCrawl/piTEDtranslate.csv','r')
    readfile = samples.readlines()
    baseurl = 'www.facebook.com/'
    # for idx in range(1, len(readfile)):

    startrow = 10
    endrow = 11
    for idx in range(startrow, endrow):
        # urls.append(baseurl+readfile[idx].split(',')[1])
        urls.append(readfile[idx].split(',')[1])
    url_num = readfile.__len__()
    print "urls: " + str(url_num)
    print "maks: " + str(url_num)

    # url_cal for record how many url already visit in this login
    url_cal = 0

    # driver init
    driver = webdriver.Firefox()
    # driver = webdriver.Chrome('C:/chromedriver') # works in windows
    # Set the timeout for the driver and socket.
    # driver.set_page_load_timeout(30)
    # socket.setdefaulttimeout(20)

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

    # kok ga berhenti ketika semua link uda dibuka

    # visit the url
    for userid in urls:
        url_cal += 1
        time.sleep(3)

        url = baseurl+userid
        print(url)
        # you should know how long you scroll in this timeline - for set the timeout
        # Print the start time.
        print time.strftime('%Y-%m-%d %A %X %Z',time.localtime(time.time()))
        # Record the start time.
        starttime = datetime.datetime.now()
        # Wait 3 seconds for the browser loading the Webpage.
        # time.sleep(3)

        driver.get(url)
        # cari scc selector yg ada di halaman likes. supaya bisa discroll
        # tabs = ['timeline', 'likes', 'about']
        current_url = driver.current_url

        # scrollLikePage(current_url, userid)
        # scrollAboutPage(current_url, userid)
        scrollTimelinePage(current_url, userid)


        """
        # find *Likes and *Comments
        """
        """
        try:
            # First find all the "*Likes *Comments".
            post_attribute_buttons = driver.find_elements_by_xpath("//div[@class='_3ccb']//a[@class='UFIBlingBox uiBlingBox feedbackBling UFIBlingBoxRevised']")
            # Then click all the "*Likes *Comments".
            for post_attribute_button in post_attribute_buttons:
                print post_attribute_button.text
                post_attribute_button.click()
            # Second find all the "View * more Comments".
            post_attribute_button_view_more_comments = driver.find_elements_by_xpath("//div[@class='_3ccb']"
                                                                                             "//li[@class='UFIRow UFIPagerRow UFIComponent UFIFirstCommentComponent']"
                                                                                             "//a[@class='UFIPagerLink']")
            # Then click all the "View * more Comments".
            for post_attribute_button_view_more_comment in post_attribute_button_view_more_comments:
                print post_attribute_button_view_more_comment.text
                post_attribute_button_view_more_comment.click()
        except Exception, e:
            print "Exception: " + url
            exception_file = open('commentclick_exception.txt', 'a')
            exception_file.write(url)
            exception_file.write(str(Exception)+': '+str(e))
            exception_file.close()
            continue
        """
        """
        # save webpage on targeted folder
        try:
            target_name = str(driver.find_element_by_id("fb-timeline-cover-name").text)
            if '\n' in target_name:
                target_name = target_name.split('\n')[0]
            page_html = driver.page_source
            # page_html_file = open('all_2015/'+target_name+' post.html', 'w')
            page_html_file = open(directory+'/'+target_name+'_post.html', 'w')
            page_html_file.write(page_html)
            page_html_file.close()
        except Exception, e:
            print "File Exception: " + url
            exception_file = open('file_exception.txt', 'a')
            exception_file.write(url)
            exception_file.write(str(Exception)+': '+str(e))
            exception_file.close()
            continue
        """
import urllib2
from bs4 import BeautifulSoup

with open("Cedo Petko post.html", "r") as testfile:
    soup_test = BeautifulSoup(testfile, "html5lib")

print soup_test.find("div")
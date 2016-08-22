# coding: utf-8

import os
import urllib
from bs4 import BeautifulSoup

base_directory = "beauty/"
start_url = "http://www.du114.com/tag/29.html"
start_page = urllib.urlopen(start_url)
soup = BeautifulSoup(start_page, "lxml")

all_pages_urls = set()
for li in soup.find("div", class_="pages").find_all("li"):
    root_url = "/".join(start_url.split("/")[:-2]) + "/"
    if li.a.get("href") and li.a.get("href") != "#":
        all_pages_urls.add(root_url + li.a.get("href"))

picset_urls = set()
for each_page_url in all_pages_urls:
    each_html = urllib.urlopen(each_page_url)
    each_soup = BeautifulSoup(each_html, "lxml")
    for item in each_soup.find_all("span", class_="both title"):
        index_url = item.a.get("href")
        if index_url:
            picset_urls.add(index_url)

for picset in picset_urls:
    index = urllib.urlopen(picset)
    base_url = "/".join(index.geturl().split("/")[:-1]) + "/"
    index_soup = BeautifulSoup(index, "lxml")
    download_directory = index_soup.h1.get_text()
    
    follow = index_soup.find("a", text="下一页")["href"]
     
    i = 1
    while follow != "#":
        try:
            src = index_soup.find("p", align="center").img.get("src")
        except:
            print "图片获取失败"
        filename = src.split("/")[-1]
        path = base_directory + download_directory + "/" + filename
        directory = os.path.dirname(path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        try:
            urllib.urlretrieve(src, path)
            print download_directory
            print "第%s张图片下载成功" % i 
            i += 1
        except:
            print "failure!!!"
        next_url = base_url + follow 
        index = urllib.urlopen(next_url)
        index_soup = BeautifulSoup(index, "lxml")
        follow = index_soup.find("a", text="下一页")["href"]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 22:45:04 2024

@author: phoebelemon
"""

import requests
import time
import os
import json
import urllib

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#############################################
thumbnails = []
captions = []
likes = []
DATA = []
filepath = "test.json"
terms = ['民族', '少数民族', '民族风', '民族风情', '56各民族服便装', '少数民族服装', 
         '民族文化', '文明民族', '不文明', '旅游推存', '文明旅游', '中国文明故事']
search_term = '民族'
post_count = 50

# each item in data is a Post object


class Post:
    def __init__(self, index, term):
        self.index = index
        self.search_term = term
        self.caption = ''
        self.author = ''
        self.likes = ''
        self.comments = []
        self.thumb_link = ''
        self.video_link = ''
        self.thumb_path = ''
        self.video_path = ''

    def __str__(self):
        return self.caption


def safe_open(path, is_asset):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if is_asset:
        return open(path, 'wb')
    else:
        return open(path, 'w', encoding='utf8')


def create_json():
    with safe_open("data/test.json", False) as f:
        json.dump([ob.__dict__ for ob in DATA], f, ensure_ascii=False)
    f.close()
    print('file created')


def save_assets(post, count):
    res = requests.get(post.thumb_link)
    res_v = requests.get(post.video_link)
    with safe_open(post.thumb_path, True) as f:
        f.write(res.content)
        print('image saved')
    with safe_open(post.video_path, True) as f:
        f.write(res_v.content)
        print('video saved')
    f.close()


# def login(username, password):
#     driver.find_element(By.CSS_SELECTOR, '.user-default').click()
#     number = driver.find_element(By.CSS_SELECTOR, '.pl-input-text')
#     number.click()
#     number.send_keys('13120986851')
    
#     driver.find_element(By.CSS_SELECTOR, '.get-verification').click()


def search_hashtag(driver, search_term):
    '''function that takes the driver object and the search term(hashtag)
    and types it into the search bar'''
    search_bar = driver.find_element(By.CSS_SELECTOR, '.search-input')
    search_bar.click()
    time.sleep(2)
    search_bar.clear()
    time.sleep(2)
    search_bar.send_keys(search_term+Keys.ENTER)


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get('https://www.kuaishou.com')
    time.sleep(3)  # wait for page to load

    # bypassing bot detection by 'pausing' the driver,
    input('press any key: ')
    # we close the bot detec window and then respond to
    # Python input
    # searching something
    search_hashtag(driver, search_term)
    input('press any key: ')
    time.sleep(2)
    # get the first video and click into it
    selected = driver.find_element(By.CSS_SELECTOR, '.video-card')
    selected.click()
    time.sleep(1)


    input('press any key: ')
    for i in range(post_count):
        try: 
            # click on first post, collect its data, and keep scrolling until
            # the specified amount of posts
            p = Post(i, search_term)
            p.index = i
            p.caption = driver.find_element(
                By.CSS_SELECTOR, '.video-info-title').text
            p.author = driver.find_element(
                By.CSS_SELECTOR, '.profile-user-name-title').text
    
            p.video_link = driver.find_element(
                By.CSS_SELECTOR, '.player-video').get_attribute('src')
            p.video_path = "data/"+p.search_term + \
                "/videos/"+p.search_term+str(i)+"vid.mp4"
    
            p.thumb_link = driver.find_element(
                By.CSS_SELECTOR, '.video-container-player').get_attribute('poster')
            p.thumb_path = "data/"+p.search_term + \
                "/thumbnails/"+p.search_term+str(i)+"img.jpg"
    
            # getting the likes and converting them to integers
            likes = driver.find_element(By.CSS_SELECTOR, '.item-count').text
            if likes[-1] == '万':
                p.likes = int(float(likes[0:-1])*10000)
            else:
                p.likes = int(likes)
    
            # checking to see if there are comments and adding the first comment
            # has_comments = driver.find_element(
            #     By.CSS_SELECTOR, '.no-comment-tip').get_attribute('style')
    
            # if has_comments != 'display: none':
            #     print('this video has comments')
            #     root_comment = driver.find_element(By.CSS_SELECTOR, '.comment-item')
            #     p.comment = root_comment.find_element(By.CSS_SELECTOR, '.comment-item-content').text
            # else: 
            #     p.comment = []
                
            DATA.append(p)  # append object to the list
            save_assets(p, post_count)  #save the video and thumbnail
            driver.find_element(By.CSS_SELECTOR, '.video-switch-next').click()
            time.sleep(1)
        except Exception as e: 
            input('press any key: ')
            print(e)
            break 
        

    create_json()
    driver.close()

    # for i in DATA:
    #     print(i)
    # comment-item
    # comment-item-body
    # sub-comment-wrap

    # comment-item-operation-op
# 13120986851

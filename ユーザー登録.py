import base64
import os
import configparser
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


import getpass
import time
import datetime
print("ユーザー登録")
user=input("user:")
password=input("password:")


options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome("ApplicationData/chrome-webdriver/chromedriver.exe", options=options)
driver.get("https://cas.ecs.kyoto-u.ac.jp/cas/login")

try:
    elem_search_word = driver.find_element_by_id("username")
    elem_search_word.send_keys(user)
    elem_search_word = driver.find_element_by_id("password")
    elem_search_word.send_keys(password)
    elem_search_btn = driver.find_element_by_name("submit")
    elem_search_btn.click()
    driver.get("https://panda.ecs.kyoto-u.ac.jp/portal/login/")

    sites=driver.find_element_by_link_text("サイトセットアップ")
    sites.click()
    
    print("login OK")
    print("ユーザー認証成功")

    euser=encode("pand",user)
    epass=encode("pand",password)


    conf = configparser.ConfigParser()
    if os.path.exists(INI):
        conf.read(INI)
    if not "user" in conf.sections():
        conf.add_section("user")
    conf.set("user","user" , euser)
    conf.set("user","password", epass)
    # ファイルに書き込む
    try:
        f = open(INI, "w")
        conf.write(f)
        f.close()
        print("ユーザー登録成功")
    except:
        print("Cant open fielError")
except:
    print("login_NG")
    print("ユーザー認証失敗")
    print("ユーザー登録失敗")

import sys
sys.exit()
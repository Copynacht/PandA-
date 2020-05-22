import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


import getpass
import time
import datetime
import base64

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome("chrome-webdriver/chromedriver.exe", options=options)
driver.get("https://cas.ecs.kyoto-u.ac.jp/cas/login")

import configparser
ini = configparser.ConfigParser()
ini.read('data/user.ini', 'UTF-8')

try:
    elem_search_word = driver.find_element_by_id("username")
    elem_search_word.send_keys(user)
    elem_search_word = driver.find_element_by_id("password")
    elem_search_word.send_keys(password)
    elem_search_btn = driver.find_element_by_name("submit")
    elem_search_btn.click()
    if __name__ == '__main__':
        start = time.time()
    driver.get("https://panda.ecs.kyoto-u.ac.jp/portal/login/")
    ############################################################################
    alltask=list()
    allitem=list()
    sites=driver.find_element_by_link_text("サイトセットアップ")
    sites.click()
    print("login OK")
except:
    print("login NG")
iframe = driver.find_element_by_css_selector("iframe")
driver.switch_to.frame(iframe)
page_element = driver.find_element_by_name('selectPageSize')
page_select_element = Select(page_element)
page_select_element.select_by_value('500')
allitem=driver.find_element_by_name("sitesForm").find_elements_by_tag_name("tr")
driver.switch_to.default_content()
length=len(allitem)
for item in range(2,length):
    task=0
    did=0
    deadline=0
    driver.get("https://panda.ecs.kyoto-u.ac.jp/portal/site/")
    sites=driver.find_element_by_link_text("サイトセットアップ")
    sites.click()
    iframe = driver.find_element_by_css_selector("iframe")
    driver.switch_to.frame(iframe)
    page_element = driver.find_element_by_name('selectPageSize')
    page_select_element = Select(page_element)
    page_select_element.select_by_value('500')

    allitem=driver.find_element_by_name("sitesForm").find_elements_by_tag_name("tr")
    allsubject=allitem[item].find_elements_by_tag_name("a")
    subject=allsubject[0].text
    allsubject[0].click()
    try:
        todo=driver.find_element_by_partial_link_text("課題")
        todo.click()
        iframe = driver.find_element_by_css_selector("iframe")
        driver.switch_to.frame(iframe)
        row=list()
        row=driver.find_element_by_name("listAssignmentsForm").find_elements_by_tag_name("tr")
        column = list()
        column = driver.find_element_by_name("listAssignmentsForm").find_elements_by_tag_name("th")
        for num in range(len(column)):
            if(column[num].text==u"課題タイトル"):
                task=num
            if(column[num].text==u"状態"):
                did=num
            if(column[num].text==u"締切"):
                deadline=num
        if(len(row)!=1):
            for num in range(1,len(row)):
                boxcolumnitem=list()
                boxcolumnitem=row[num].find_elements_by_tag_name("td")
                if(boxcolumnitem[did].text=="未開始"):
                    date_str=boxcolumnitem[deadline].text
                    if("N/A" not in date_str and len(date_str)!=0):
                        date_dt = datetime.datetime.strptime(date_str, '%Y/%m/%d %H:%M')
                        nowtime=datetime.datetime.now()
                        if(nowtime<date_dt):
                            constructedtask=date_dt.strftime('%Y/%m/%d %H:%M')+"|"+"　　課題　　|"+subject+"・・・"+boxcolumnitem[task].text
                            nowtime=nowtime+datetime.timedelta(days=1)
                            if(nowtime>date_dt):
                                constructedtask="△|"+constructedtask
                            else:
                                constructedtask="〇|"+constructedtask
                            alltask.append(constructedtask)
                            print(constructedtask)
                    if("N/A" in date_str or len(date_str)==0):
                        constructedtask="〇|"+date_str+"|"+"　　課題　　|"+subject+"|"+boxcolumnitem[task].text+"・・・"+boxcolumnitem[did].text
                        alltask.append(constructedtask)
                        print(constructedtask)
        driver.switch_to.default_content()
    except selenium.common.exceptions.NoSuchElementException:
        driver.switch_to.default_content()
    try:
        quiz=driver.find_element_by_partial_link_text("テスト")
        quiz.click()
        iframe = driver.find_element_by_css_selector("iframe")
        driver.switch_to.frame(iframe)
        row=list()
        row=driver.find_element_by_id("selectIndexForm:selectTable").find_elements_by_tag_name("tr")
        column = list()
        column = driver.find_element_by_id("selectIndexForm:selectTable").find_elements_by_tag_name("th")
        for num in range(len(column)):
            if(column[num].text==u"タイトル"):
                task=num
            if(column[num].text==u"締切日時"):
                deadline=num
        if(len(row)!=1):
            for num in range(1,len(row)):
                boxcolumnitem=list()
                boxcolumnitem=row[num].find_elements_by_tag_name("td")
                date_str=boxcolumnitem[deadline].text
                if("午後" in date_str):
                    date_str=date_str.replace(' 午後','')
                    date_dt = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')
                    date_dt=date_dt+datetime.timedelta(hours=12)
                if("午前" in date_str):
                    date_str=date_str.replace(" 午前","")
                    date_dt = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')
                nowtime=datetime.datetime.now()
                if(nowtime<date_dt):
                    nowtime=nowtime+datetime.timedelta(days=1)
                    constructedtask=date_dt.strftime('%Y/%m/%d %H:%M')+"|"+"テストクイズ"+"|"+subject+"・・・"+boxcolumnitem[task].text
                    if(nowtime>date_dt):
                        constructedtask="△|"+constructedtask
                    else:
                        constructedtask="〇|"+constructedtask
                    alltask.append(constructedtask)
                    print(constructedtask)
                if("N/A" in date_str or len(date_str)==0):
                    constructedtask="〇|"+date_str+"|"+"テストクイズ"+"|"+subject+"・・・"+boxcolumnitem[task].text
                    nowtime=nowtime+datetime.timedelta(days=1)
                    alltask.append(constructedtask)
                    print(constructedtask)
    except selenium.common.exceptions.NoSuchElementException:
        driver.switch_to.default_content()
print("=================================================")
alltask.sort()
path = 'data/task.txt'
f = open(path,'w',encoding='Shift_JIS',errors='ignore')
for x in range(len(alltask)):
    print(alltask[x])
    f.write(alltask[x]+"\n")
f.close()

import sys
sys.exit()

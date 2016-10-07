#! /usr/bin/python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.common.keys import Keys

import time
import os
import sys
import logging
import httplib
import urllib
import pickle
import urllib2

def debug2(str):
    logging.error(": " + str)
    return

def goCrew(url,aid,cityCode):
    url_list=[]
    data_list=[]
    page = 1

    aid=aid;
    
    driver.set_page_load_timeout(50)
    try:
        driver.get(url)
    except:
        print "excption on get url:"+url
        return

    page_title = driver.title

    newUrl = "http://www.dianping.com/search/category/"+cityCode+"/75"
    driver.get(newUrl)
    print driver.title
    time.sleep(5)
    
    print "begin to collection:"
    while True:
        for e in ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"]:
            try:
                oUlParents = driver.find_element_by_id("shop-all-list")
                oUl = oUlParents.find_element_by_xpath('./ul')
                oli = oUl.find_element_by_xpath('./li['+e+']')
                oImg = oli.find_element_by_xpath('./div[1]/a/img')
                    
                #src:
                # collPicSrc = oImg.get_attribute('src')
                #title
                oTitle = oli.find_element_by_xpath('./div[2]/div[1]/a/h4').text
                #address
                oAddress = oli.find_element_by_xpath('./div[2]/div[3]/span[1]').text
                #cellphoneURL
                oCellphoneHref = oli.find_element_by_xpath('./div[2]/div[1]/a').get_attribute('href')

                print "*************************************page:"+str(page)+":"+str(int(e))+"*************************************"
                # print collPicSrc
                print oTitle
                print oAddress
                
                time.sleep(5)
                obj={}
                # obj['src']=collPicSrc
                obj['title']=oTitle
                obj['address']=oAddress
                data_list.append(obj)
                url_list.append(oCellphoneHref)
                time.sleep(5)
            except:
                continue

        index = 0
        for e in url_list:
            try:
                driver.get(e)
                time.sleep(5)
                oTelephoneParents = driver.find_element_by_class_name('book')
                oTelephone = oTelephoneParents.find_element_by_xpath('./div/span').text
                print oTelephone 
                data_list[index]['tel']=oTelephone
                index = index+1
                time.sleep(5)
            except:
                oTelephone= 'NULL'  
                print oTelephone 
                data_list[index]['tel']=oTelephone
                index = index+1
                time.sleep(5)
                continue
        fout = open('nj.txt','a')
        for item in data_list:
            a = item['title'].encode('utf8')+','+item['address'].encode('utf8')+','+item['tel'].encode('utf8')+','+'\r\n'+'\r\n'
            fout.write(a)
        fout.close()
        # clear []
        url_list=[]
        data_list=[]
        
        if(page>=50):
            fout.close()
            break
        
        page = page + 1
      
        driver.get("http://www.dianping.com/search/category/"+cityCode+"/75/p"+str(page)+"?"+aid)
        time.sleep(10)
        
driver = webdriver.Firefox()
print 'start'
driver.set_page_load_timeout(10)
goCrew("http://www.dianping.com/",'aid=18619099%2C66796043%2C67321127%2C59179054%2C67663786%2C57924112',5)

driver.quit()
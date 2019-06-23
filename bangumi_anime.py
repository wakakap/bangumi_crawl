#未登录状态下爬取某用户看过的动画的信息村委csv文件
from selenium import webdriver
import csv
import requests  
import time

csv_file = open("animelist.csv","w",newline='',encoding="utf-8")
writer = csv.writer(csv_file)
writer.writerow(['CHN_NAME','ORI_NAME','RELEASE_TIME','MY_TAG','LINK','MY_STAR','MY_COMMENT'])
page=1
while 1:
    print("page is "+str(page))
    URL = 'http://bangumi.tv/anime/list/wakakap/collect?page='+str(page)
    driver = webdriver.PhantomJS(executable_path='C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\Scripts\phantomjs.exe')
    driver.get(URL)
    #driver.switch_to.frame("")这个html没有使用frame所以不需要跳转
    #我尝试了搜索classname定位，总是报错，估计这种方法有些问题。
    #改用绝对路径方法。
    #用css_selector方法注意：
    #driver.find_element_by_css_selector(‘.class_value’)这种方法尝试后报错不清楚为什么
    #######注意class有空格时写一边就够了####
    #driver.find_element_by_css_selector(‘tag_name.class_value’)这种方法可行，甚至当tag_name唯一时可省略.class_value
    data = driver.find_element_by_id("browserItemList")
    i=1
    try: 
        data.find_element_by_xpath('/html/body/div/div/div/div/ul/li[1]/div')
    except Exception:
        break
    while 1:
        try:
            item = data.find_element_by_xpath('/html/body/div/div/div/div/ul/li['+str(i)+']/div')
        except Exception:
            break
        link = item.find_element_by_css_selector("a").get_attribute('href')
        chn_name = item.find_element_by_css_selector("a").text
        try:
            ori_name = item.find_element_by_css_selector("small.grey").text
        except Exception:
            ori_name =chn_name
        try:
            sstar = item.find_element_by_css_selector("span.starsinfo")
            star = sstar.get_attribute('class')
            startext=0
            if star=='sstars1 starsinfo':
                startext=1
            elif star=='sstars2 starsinfo':
                startext=2
            elif star=='sstars3 starsinfo':
                startext=3
            elif star=='sstars4 starsinfo':
                startext=4
            elif star=='sstars5 starsinfo':
                startext=5
            elif star=='sstars6 starsinfo':
                startext=6
            elif star=='sstars7 starsinfo':
                startext=7
            elif star=='sstars8 starsinfo':
                startext=8
            elif star=='sstars9 starsinfo':
                startext=9
            elif star=='sstars10 starsinfo':
                startext=10
        except Exception:
            startext=0
            print("error")
        #str.find(str, beg=0, end=len(string))
        try:
            inform = item.find_element_by_css_selector("p.info").text
        except Exception:
            inform = "标签: NONE"
        ttag = item.find_element_by_css_selector("p.collectInfo").text
        try:
            mycom = item.find_element_by_css_selector("div.text").text
        except Exception:
            mycom = 'NONE'
        a1=inform.find('/')
        a2=inform.find('/',a1+1)
        rel_time=inform[a1+2:a2-1]
        b1=ttag.find('标签:')
        tag=ttag[b1+4:]
        #print("i is "+str(i))
        #print(link)
        #print(chn_name)
        #print(rel_time)
        #print(ori_name)
        #print(tag)
        #print(mycom)
        #print(startext)
        #write
        try:
            row = [chn_name,ori_name,rel_time,tag,link,startext,mycom]
            writer.writerow(row)
        except Exception:
            print('error!!!!!!!!!!!')
        i=i+1
    page=page+1
csv_file.close()
print('finished！')
time.sleep(60)

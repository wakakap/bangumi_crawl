#爬取某用户看过的动画的信息存为csv文件
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import requests  
import time
csv_file = open("myanimelist.csv","w",newline='',encoding="utf-8")
writer = csv.writer(csv_file)
writer.writerow(['CHN_NAME','ORI_NAME','INFO','MY_TAG','LINK','MY_STAR','MY_COMMENT'])
#f12->network->doc->点击name下的名称->cookies抄写于此
#目前还没有理解透彻cookie
#试错法得到：优先写浏览器查看的response cookie，如没有写request cookie的后三个。
cookie1={'domain':'.bangumi.tv',
        'name':'chii_sid',
        'value':'zMSwDd',
        'path':'/'}
cookie2={'domain':'.bangumi.tv',
        'name':'chii_theme',
        'value':'light',
        'path':'/'}
cookie3={'domain':'.bangumi.tv',
        'name':'chii_auth',
        'value':'Z16qEam2WhNzf7XGW1i%2BmOzFLgAnH0qgzlVal4A7oe3UNEj4%2BtpmbEeZZg%2B2elBC7X3elwGf9ps2KabeAvxhVmBHQihUeQMoxAR9	',
        'path':'/'}
cookie4={'domain':'.bangumi.tv',
        'name':'chii_cookietime',
        'value':'2592000',
        'path':'/'}
page=1
sum=0
ersum=0
URL = 'https://bangumi.tv/anime/list/wakakap/collect?page='+str(page)
#driver = webdriver.PhantomJS(executable_path='C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\Scripts\phantomjs.exe')
#chrome_options = Options()
#chrome_options.add_argument('--headless')#无头模式
#driver = webdriver.Chrome(chrome_options=chrome_options)
driver = webdriver.Chrome()
driver.get(URL)
########手动登录######
time.sleep(40)#
# 获取cookies
cookie_list = driver.get_cookies()
driver.get(URL)
##使用cookie部分###############################
#driver.delete_all_cookies()
#driver.add_cookie(cookie1)
#driver.add_cookie(cookie2)
#driver.add_cookie(cookie3)
#driver.add_cookie(cookie4)
#driver.get(URL)#注意用这种方法时要二次get
###############################################
while 1:
    print("page is "+str(page))
    URL = 'https://bangumi.tv/anime/list/wakakap/collect?page='+str(page)
    driver.get(URL)
    #driver.switch_to.frame("")这个html没有使用frame所以不需要跳转
    #我尝试了搜索classname定位，总是报错，估计这种方法有些问题。
    #改用绝对路径方法。
    #用css_selector方法注意：
    #driver.find_element_by_css_selector(‘.class_value’)这种方法尝试后报错不清楚为什么
    #######注意class有空格时写一边就够了####
    #driver.find_element_by_css_selector(‘tag_name.class_value’)这种方法可行，甚至当tag_name唯一时可省略.class_value
    data = driver.find_element_by_id("browserItemList")
    try: 
        data.find_element_by_xpath('/html/body/div/div/div/div/ul/li[1]/div')
    except Exception:
        break
    i=1
    while 1:
        try:
            item = data.find_element_by_xpath('/html/body/div/div/div/div/ul/li['+str(i)+']/div')
        except Exception:
            break
        link = item.find_element_by_css_selector('h3').find_element_by_css_selector("a").get_attribute('href')
        t_name = item.find_element_by_css_selector('h3').find_element_by_css_selector("a").text
        try:
            ori_name = item.find_element_by_css_selector('h3').find_element_by_css_selector("small.grey").text
            chn_name=t_name
        except Exception:
            ori_name = t_name
            chn_name = 'NONE'
        try:
            sstar = item.find_element_by_css_selector("span.starlight")
            star = sstar.get_attribute('class')
            startext=0
            if star=='starlight stars1':
                startext=1
            elif star=='starlight stars2':
                startext=2
            elif star=='starlight stars3':
                startext=3
            elif star=='starlight stars4':
                startext=4
            elif star=='starlight stars5':
                startext=5
            elif star=='starlight stars6':
                startext=6
            elif star=='starlight stars7':
                startext=7
            elif star=='starlight stars8':
                startext=8
            elif star=='starlight stars9':
                startext=9
            elif star=='starlight stars10':
                startext=10
        except Exception:
            startext=-1
            print('start error '+str(startext))
        #str.find(str, beg=0, end=len(string))
        #inform
        try:
            inform = item.find_element_by_css_selector("p.info").text
        except Exception:
            inform = "NONE"
        #tag
        try:
            ttag = item.find_element_by_css_selector("p.collectInfo").text
        except Exception:
            ttag = '标签: NONE'
        #mycom
        try:
            mycom = item.find_element_by_css_selector("div.text").text
        except Exception:
            mycom = 'NONE'
        #a1=inform.find('/')
        #a2=inform.find('/',a1+1)
        #rel_time=inform[a1+2:a2-1]
        b1=ttag.find('标签:')
        tag=ttag[b1+4:]
        sum=sum+1
        print("page;i;sum is "+str(page)+' '+str(i)+' '+str(sum))
        print(ori_name)
        #print(chn_name)
        #print(inform)
        #print(link)
        #print(tag)
        #print(mycom)
        #print(startext)
        try:
            row = [chn_name,ori_name,inform,tag,link,startext,mycom]
            writer.writerow(row)
        except Exception:
            ersum=ersum+1
            row = ['error','page is '+str(page),'i is '+str(i),'sum is '+str(sum),'','','']
            writer.writerow(row)
        i=i+1
    page=page+1
csv_file.close()
print('finished！')
time.sleep(60)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import json
from linebot.models import *
from flex_msg import *
from config import *
import time
import random
import string


def car_8891_info(keyword):
    #建立url跟目錄
    url = 'https://tw.usedcar.yahoo.com/'
    #建立chrome設定
    chromeOption = webdriver.ChromeOptions()
    #設定瀏覽器的user agent
    #chromeOption.add_argument('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
    chromeOption.add_argument("start-maximized")
    #chromeOption.add_argument('--headless')
    chromeOption.add_argument('--no-sandbox')
    chromeOption.add_argument('--incognito')
    chromeOption.add_argument('--disable-dev-shm-usage')
    #開啟Chrome瀏覽器
    driver = webdriver.Chrome(options=chromeOption)
    #調整瀏覽器視窗大小
    driver.set_window_size(1024, 960)


    # 進入指定網址
    driver.get(url)

    # 定義一個物件
    typing = driver.find_element_by_xpath('//*[@name="kw"]')
    typing.send_keys(keyword)
    time.sleep(1)

    # 按下輸入搜尋按鈕
    typing.send_keys(Keys.RETURN)
    time.sleep(2)

    # 等待網頁讀取

    # ======================從網頁獲取前十個連結===========================

    # 建立文章url列表
    car_info_url_list = []
    # 取得連結
    car_yahoo_url = driver.find_elements(By.CSS_SELECTOR, ".infos.mei-u > p.vmlist > a")
    print(len(car_yahoo_url))
    for url in car_yahoo_url:
        if len(car_info_url_list) < 10:
            car_info_url_list.append(url.get_attribute('href'))
            print(url.get_attribute('href'))


    # ======================從網頁獲得前十張縮圖===========================

    # 滾動視窗捲軸，使瀏覽器獲取影片縮圖資訊
    for i in range(20):
        y_position = i * 100
        driver.execute_script(f'window.scrollTo(0, {y_position});')
        time.sleep(0.1)

    #建立縮圖列表
    car_info_images_list = []

    # 取得縮圖(需滾動頁面)
    car_yahoo_pic = driver.find_elements(By.CSS_SELECTOR, ".preview.mei-u > a > img")
    print(len(car_yahoo_pic))
    for image in car_yahoo_pic:
        if len(car_info_images_list) < 10:
            car_info_images_list.append(image.get_attribute('src'))
            print(image.get_attribute('src'))


    # ======================從網頁獲取前十個標題===========================

    #建立標題列表
    car_info_title_list = []

    # 取得標題
    car_yahoo_title = driver.find_elements(By.CSS_SELECTOR, ".infos.mei-u > p.vmlist > a")
    print(len(car_yahoo_title))
    for infos in car_yahoo_title:
        if len(car_info_title_list) < 10:
            car_info_title_list.append(infos.get_attribute('title'))
            print(infos.text)

    # ===================從網頁獲取前十個價錢========================
    #建立頻道資訊列表(價錢)
    car_info_price_list = []

    # 取得價錢
    car_yahoo_price = driver.find_elements(By.CSS_SELECTOR, ".infowrap.mei-g > span:nth-child(1) > em.price")
    print(len(car_yahoo_price))
    for prices in car_yahoo_price:
        if len(car_info_price_list) < 10:
            car_info_price_list.append(prices.text)
            print(prices.text)

    # ===================從網頁獲取前十個年份========================
    #建立頻道資訊列表(價錢)
    car_info_years_list = []

    # 取得年份
    car_yahoo_year = driver.find_elements(By.CSS_SELECTOR, ".mei-g > span:nth-child(2) > span > span:nth-child(1)")
    print(len(car_yahoo_year))
    for year in car_yahoo_year:
        if len(car_info_years_list) < 10:
            car_info_years_list.append(year.text)
            print(year.text)

    # ===================從網頁獲取前十個里程========================
    #建立頻道資訊列表(價錢)
    car_info_kms_list = []

    # 取得里程
    car_yahoo_km = driver.find_elements(By.CSS_SELECTOR, ".mei-g > span:nth-child(2) > span > span:nth-child(2)")
    print(len(car_yahoo_km))
    for kms in car_yahoo_km:
        if len(car_info_kms_list) < 10:
            car_info_kms_list.append(kms.text)
            print(kms.text)

    # ===================從網頁獲取前十個地區========================
    #建立頻道資訊列表(價錢)
    car_info_locat_list = []

    # 取得地點
    car_yahoo_locat = driver.find_elements(By.CSS_SELECTOR, ".infowrap.mei-g > span:nth-child(3)")
    print(len(car_yahoo_locat))
    for locat in car_yahoo_locat:
        if len(car_info_locat_list) < 10:
            car_info_locat_list.append(locat.text)
            print(locat.text)

    # ===================從網頁獲取前十個刊登者========================
    #建立頻道資訊列表(價錢)
    car_info_writer_list = []

    # 取得作者
    car_yahoo_writer = driver.find_elements(By.CSS_SELECTOR, ".infowrap.mei-g > span:nth-child(5) > a")
    print(len(car_yahoo_writer))
    for writer in car_yahoo_writer:
        if len(car_info_writer_list) < 10:
            car_info_writer_list.append(writer.text)
            print(writer.text)


    #關閉瀏覽器連線
    driver.close()

    #==============將爬取到的資訊以FlexMessage回傳至主程式===================
    message = []

    #回傳搜尋結果的FlexMessage
    message.append(image_carousel('車款搜尋結果', car_info_url_list, car_info_images_list, car_info_title_list, car_info_price_list, car_info_years_list, car_info_kms_list, car_info_locat_list, car_info_writer_list))
    return message
   
    
#可於本機中直接執行python web_crawler.py進行單元測試，但必須先將CHANNEL_ACCESS_TOKEN、USERID都在config.py設定好
if __name__=='__main__':
    from linebot import LineBotApi, WebhookHandler
    from linebot.exceptions import InvalidSignatureError
    from linebot.models import *
    message = car_8891_info('2016 nissan')
    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    line_bot_api.push_message(USERID,message)
    

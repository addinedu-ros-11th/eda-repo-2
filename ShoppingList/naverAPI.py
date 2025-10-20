#-*- coding: utf-8 -*-
import os
import sys
import urllib.request
import json
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

import pandas as pd

def clickAndFindLoop(ind, ele, level, parent_id, driver):
    cat = {}
    cat['id']= int(ele['data-cid'])
    cat['p_id'] = int(parent_id)
    cat['name'] = ele.get_text()
    cat['level'] = level
    print(cat['id'], cat['p_id'], cat['name'], cat['level'])

    # 1차 dropdown 열기
    try:
        span = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[{level}]/span'))
            )
        span.click()
        # 1차 카테고리 선택
        choose = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//*[@id="content"]/div[2]/div/div[1]/div/div/div[1]/div/div[{level}]/ul/li[{ind+1}]/a'))
        )
        choose.click()
        time.sleep(0.5)

        next_soup = BeautifulSoup(driver.page_source, 'html.parser')
        next_data = next_soup.find_all('div',  'set_period category')[0].find_all('ul', 'select_list scroll_cst')[level].find_all('a', 'option')
    except:
        next_data = None
        print(next_data)
    return cat, driver, next_data


def generateCatId():


    driver_path = Path('ShoppingList/driver/chromedriver')
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service)
    
    datalab_url = 'https://datalab.naver.com/shoppingInsight/sCategory.naver'
    driver.get(datalab_url)
    time.sleep(3)

    # first and second catid
    
    first_soup = BeautifulSoup(driver.page_source, 'html.parser')
    first_data = first_soup.find_all('div',  'set_period category')[0].find_all('ul', 'select_list scroll_cst')[0].find_all('a', 'option')
    cat_list = []

    for i, ele in enumerate(first_data):
        cat, driver, second_data = clickAndFindLoop(i, ele, level=1, parent_id=0, driver=driver)
        cat1_id = cat['id']
        cat_list.append(cat)

        if second_data is not None:
            for i1, ele1 in enumerate(second_data):
                cat, driver, third_data = clickAndFindLoop(i1, ele1, 2, parent_id=cat1_id, driver=driver)
                cat2_id = cat['id']
                cat_list.append(cat)

                if third_data is not None:
                    for i2, ele2 in enumerate(third_data):
                        cat, driver, fourth_data = clickAndFindLoop(i2, ele2, 3, parent_id=cat2_id, driver=driver)
                        cat_list.append(cat)
                        cat3_id = cat['id']

                        if fourth_data is not None:
                            for ele3 in fourth_data:
                                cat = {}
                                cat['id']= int(ele3['data-cid'])
                                cat['p_id'] = cat3_id
                                cat['name'] = ele3.get_text()
                                cat['level'] = 4
                                print(cat['id'], cat['p_id'], cat['name'])
                                cat_list.append(cat)
                        else:
                            continue
                else:
                    continue
        else:
            continue



            
    driver.quit()
    return cat_list


def fetchShoppingDataFromNaver(client_id, client_secret,startDate, endDate, timeUnit, categoryNameCodeList, device=None, ages=None, gender=None):
    

    #print(client_secret,client_id)
    url = "https://openapi.naver.com/v1/datalab/shopping/categories"

    body_dict = {
        "startDate": startDate,
        "endDate": endDate,
        "timeUnit": timeUnit,
        "category": categoryNameCodeList,
    }
    if device is not None and device != "":
        body_dict["device"] = device
    if ages is not None and len(ages) > 0:
        body_dict["ages"] = ages
    if gender is not None and gender != "":
        body_dict["gender"] = gender

    body = json.dumps(body_dict)

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    request.add_header("Content-Type","application/json")
    response = urllib.request.urlopen(request, data=body.encode("utf-8"))

    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        response_decoded = response_body.decode('utf-8')
        response_data = json.loads(response_decoded)
        with open("ShoppingList/output/naver_result.json", "w", encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False, indent=4)
    else:
        print("Error Code:" + rescode)

if __name__ == '__main__':

    a = 1

    if a ==  0:
        #example
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(current_dir, '..', '.env')
        load_dotenv(dotenv_path=dotenv_path)
        client_id = os.getenv("NAVER_CLIENT_ID")
        client_secret = os.getenv("NAVER_CLIENT_SECRET")
        test_category_list = [
            {"name":"신선식품", "param": ["10000108"]}, 
            {"name":"가공식품", "param": ["50000002"]},
            {"name":"건강식품", "param": ["10000115"]}
        ]
        fetchShoppingDataFromNaver(client_id,client_secret,"2025-10-02", "2025-10-09", "date",test_category_list)
    elif a ==1 :
        catlist = generateCatId()
        with open('ShoppingList/output/naverCategoryTable_temp.json', 'w', encoding='utf-8') as f:
            json.dump(catlist, f, ensure_ascii=False, indent=4)
    else:
        pass

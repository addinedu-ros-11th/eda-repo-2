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
import numpy as np

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

def fetchShoppingDataFromNaver(client_id, client_secret,startDate, endDate, timeUnit, categoryNameCodeList, file_name, device=None, ages=None, gender=None):
    

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
        if file_name is not None:
            with open(file_name, "w", encoding='utf-8') as f:
                json.dump(response_data, f, ensure_ascii=False, indent=4)
        #print(response_data)
        return response_data
    else:
        print("Error Code:" + rescode)

def listToCategoryDict(list):
    res = [{"name":ele[1], "param":[str(ele[0])]} for ele in list]
    return res

def extractHighestData(dict_data):
    dict_data_result = dict_data['results']
    a= {}
    for i, data_list in enumerate(dict_data_result):
        for j, data in enumerate(data_list['data']):
            if data['ratio'] == 100:
                a['category'] = data_list['category']
                a['period'] = data['period']
                a['ratio'] = data['ratio']
                a['index'] = [i, j]
                return a
    print("can't find data which ratio is 100")
    return 0

def getratio(pre_res, cur_dict_data, cur_index_of_pre: int):
    ratio = cur_dict_data['results'][cur_index_of_pre]['data'][pre_res['index'][1]]
    ratio = ratio['ratio']
    #print(type(ratio))
    return ratio

def compare_two_batches(pre_res: dict, cur_dict_data, cur_index_of_pre: int, cat_index: int, highest_cat_index: int):
    highest_data = extractHighestData(cur_dict_data)
    cur_high_cate = highest_data['category'][0]
    multiplier = 1
    if cur_high_cate != pre_res['category'][0]:
        cur_ratio_of_pre_high_data = getratio(pre_res,cur_dict_data, cur_index_of_pre)
        multiplier = cur_ratio_of_pre_high_data/100
        highest_cat_index = cat_index
    
    return multiplier, highest_cat_index, highest_data

def createTrendData(client_id, client_secret, catlist, start_date, end_date, device = None, ages=None, gender=None):
   
    num_category = len(catlist)
    cat_list_to_be_compared = []
    num_batches = num_category-1
    muliplier_list = [1. for i in range(num_category)]

    # generate first batch
    category_to_be_compared = [catlist[0],catlist[1]]
    dict_data = fetchShoppingDataFromNaver(client_id, client_secret, start_date, end_date, "date", 
                                   category_to_be_compared, None, device, ages, gender)
    pre_res = extractHighestData(dict_data)
    cat_list_to_be_compared.append(dict_data['results'][0])
    cat_list_to_be_compared.append(dict_data['results'][1])
    highest_cat_index = pre_res['index'][0]
    cat_index = 2
    batch_index = 1

    # generate batches, update multiplier list and highest cat index
    while batch_index < num_batches:
        category_to_be_compared = [catlist[highest_cat_index],catlist[cat_index]]
        dict_data = fetchShoppingDataFromNaver(client_id, client_secret, start_date, end_date, "date", 
                                   category_to_be_compared, None, device,ages,gender)
        cat_list_to_be_compared.append(dict_data['results'][1])

        # compare two batches and update higeset_cat_index
        multiply_const, highest_cat_index, pre_res = compare_two_batches(pre_res, dict_data, 0, cat_index, highest_cat_index)
        if multiply_const != 1:
            temp_muliplier_list = [x*multiply_const for x in muliplier_list[:highest_cat_index]]
            muliplier_list[:highest_cat_index] = temp_muliplier_list

        batch_index += 1
        cat_index += 1

    # multiply obtained multiply list to cat list
    for i, cat_dic_data in enumerate(cat_list_to_be_compared):
        multiply_const = muliplier_list[i]
        # for data_per_period in cat_dic_data['data']:
        #     data_per_period['ratio']=data_per_period['ratio']*multiply_const
        for i in range(len(cat_dic_data['data'])):
            cat_dic_data['data'][i]['ratio'] = cat_dic_data['data'][i]['ratio']*multiply_const

    res = {}
    res['startdate'] = start_date
    res['enddate'] = end_date
    res['datalist'] = cat_list_to_be_compared
    
    return res
    



        
    

if __name__ == '__main__': # Examples

    a = 3
    
    if a == 0: # naver api에서 트렌드 가져오기 테스트
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
        fetchShoppingDataFromNaver(client_id,client_secret,
                                   "2025-10-02", 
                                   "2025-10-09", 
                                   "date", 
                                   test_category_list, 
                                   'ShoppingList/output/example1.json')

    elif a == 1: # 카테고리 리스트 가져오기
        catlist = generateCatId()
        with open('ShoppingList/output/naverCategoryTable_temp.json', 'w', encoding='utf-8') as f:
            json.dump(catlist, f, ensure_ascii=False, indent=4)

    elif a ==2: #기존 api
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(current_dir, '..', '.env')
        load_dotenv(dotenv_path=dotenv_path)
        client_id = os.getenv("NAVER_CLIENT_ID")
        client_secret = os.getenv("NAVER_CLIENT_SECRET")

        categroy_json = pd.read_json('ShoppingList/output/naverCategoryTable.json')
        df_category = pd.DataFrame(categroy_json)
        food = df_category[df_category['p_id'] == 50000006] # 음식 카테고리
        b = food[['id','name']].to_dict('tight')
        to_be_found = np.array(b['data'])
        test_category_list = listToCategoryDict(to_be_found[[2,3,4]]) # 총 3개까지만 가능
        print(test_category_list)
        fetchShoppingDataFromNaver(client_id,client_secret,
                                   "2025-10-02", 
                                   "2025-10-09", 
                                   "date",
                                    test_category_list, 
                                    'ShoppingList/output/example3.json')
        
    elif a == 3: #개선된 api
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(current_dir, '..', '.env')
        load_dotenv(dotenv_path=dotenv_path)
        client_id = os.getenv("NAVER_CLIENT_ID")
        client_secret = os.getenv("NAVER_CLIENT_SECRET")

        categroy_json = pd.read_json('ShoppingList/output/naverCategoryTable.json')
        df_category = pd.DataFrame(categroy_json)
        food = df_category[df_category['p_id'] == 50000006] # 음식 카테고리
        b = food[['id','name']].to_dict('tight')
        to_be_found = np.array(b['data'])
        test_category_list = listToCategoryDict(to_be_found)
        print(len(test_category_list))
        res = createTrendData(client_id, client_secret,test_category_list, "2025-10-02", "2025-10-09")
        print(res)
        with open('ShoppingList/output/res_temp.json', 'w', encoding='utf-8') as f:
            json.dump(res, f, ensure_ascii=False, indent=4)


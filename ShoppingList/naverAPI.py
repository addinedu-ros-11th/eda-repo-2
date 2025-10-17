#-*- coding: utf-8 -*-
import os
import sys
import urllib.request
import json
from dotenv import load_dotenv

def generateCatId():

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

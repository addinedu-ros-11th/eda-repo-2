#-*- coding: utf-8 -*-
import os
import sys
import urllib.request
import json
from dotenv import load_dotenv

def fetchShoppingDataFromNaver(startDate, endDate, timeUnit, category_name, category_param, device, age, gender):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dotenv_path = os.path.join(current_dir, '..', '.env')
    load_dotenv()


    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")
    print(client_secret,client_id)
    url = "https://openapi.naver.com/v1/datalab/shopping/categories";
    body = '{"startDate":"2017-08-01","endDate":"2017-09-30","timeUnit":"month","category":[{"name":"패션의류","param":["50000000"]},{"name":"화장품/미용","param":["50000002"]}],"device":"pc","ages":["20","30"],"gender":"f"}'

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    request.add_header("Content-Type","application/json")
    print(request)
    response = urllib.request.urlopen(request, data=body.encode("utf-8"))

    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        response_decoded = response_body.decode('utf-8')
        print(response_decoded)
        response_data = json.loads(response_decoded)
        with open("ShoppingList/output/naver_result.json", "w", encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False, indent=4)
    else:
        print("Error Code:" + rescode)

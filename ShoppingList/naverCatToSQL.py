import mysql.connector
import os
from dotenv import load_dotenv
import json


def batchInsertFromJsonList(data_list: list[dict], table_name: str, conn) -> None:
    
    cursor = conn.cursor(buffered=True)
    sql = f"""
        INSERT INTO {table_name} (cat_id, p_id, cat_name, cat_level)
        VALUES (%s, %s, %s, %s)
    """

    # 2. 튜플 리스트 준비 (executemany를 위해)
    data_to_insert = []
    print(data_list)
    for item_dict in data_list:
        # 딕셔너리의 값을 SQL 쿼리 순서에 맞게 튜플로 만듭니다.
        row_tuple = (
            item_dict.get("id"),
            item_dict.get("p_id"),
            item_dict.get("name"),
            item_dict.get("level")
        )
        data_to_insert.append(row_tuple)

    # 3. 배치 삽입 실행
    try:
        cursor.executemany(sql, data_to_insert)
        conn.commit()
        print(f"✅ JSON 리스트의 총 {cursor.rowcount}개 항목이 DB에 삽입되었습니다.")

    except mysql.connector.Error as err:
        conn.rollback()
        print(f"❌ 데이터 삽입 중 오류 발생: {err}")
    finally:
        cursor.close()
    
if __name__ == '__main__':
    # JSON 파일을 읽어 파이썬 리스트로 변환
    try:
        with open('ShoppingList/output/naverCategoryTable.json', 'r', encoding='utf-8') as f:
            data_list = json.load(f) 
            print(f"로드된 데이터 건수: {len(data_list)}개")

    except FileNotFoundError:
        print("❌ 파일을 찾을 수 없습니다.")
    except json.JSONDecodeError:
        print("❌ JSON 파일 형식이 올바르지 않습니다.")

    load_dotenv()
    
    aws1_password = os.environ.get('AWS1_PASSWORD')

    db_connection = mysql.connector.connect(
        host = "edu-1.cpoiow8a8io6.ap-northeast-2.rds.amazonaws.com",
        port = 3306,
        user = 'root',
        password = aws1_password,
        database = 'EDA_PROJECT'
    )
    
    
    # 삽입할 딕셔너리 리스트 예시
    batchInsertFromJsonList(data_list, "naver_shopping_category", db_connection)
    db_connection.close()

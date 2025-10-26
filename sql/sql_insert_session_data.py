import mysql.connector
from dotenv import load_dotenv
import os
from datetime import date, timedelta

load_dotenv()

aws1_password = os.environ.get('AWS1_PASSWORD')

# --- 1. DB 접속 및 설정 ---
DB_CONFIG = {
    'host': "edu-1.cpoiow8a8io6.ap-northeast-2.rds.amazonaws.com", # AWS RDS 엔드포인트로 변경
    'port' : 3306,
    'user': 'root',
    'password': aws1_password,
    'database': 'EDA_PROJECT' # DB 이름으로 변경
}


# --- 2. 날짜 범위 설정 ---
start_date = date(2020, 1, 1)
end_date = date(2025, 12, 31)

# --- 3. 데이터 삽입 함수 ---

def generate_custom_id(date_obj, hour_int):
    """
    YYMMDDHH 형식의 ID를 생성합니다.
    - hour_int가 -1이면 HH 대신 99를 사용합니다.
    """
    # YYMMDD 문자열 포맷팅
    date_part = date_obj.strftime('%y%m%d')
    
    if hour_int == -1:
        # 시간 정보 없을 때: YYMMDD99
        hour_part = '99'
    else:
        # 시간 정보 있을 때: YYMMDDHH (03, 14 등)
        hour_part = f'{hour_int:02d}'
        
    # 최종 ID를 BIGINT 타입으로 저장하기 위해 정수(int)로 변환
    return int(date_part + hour_part)

def generate_and_insert_data(start_date, end_date):
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
    except mysql.connector.Error as err:
        print(f"❌ DB 연결 오류: {err}")
        return

    # SQL 삽입 쿼리 템플릿: 이제 id 컬럼도 포함하여 3개의 값을 삽입합니다.
    insert_sql = "INSERT INTO datetime_record (dt_id, s_date, s_hour) VALUES (%s, %s, %s)"
    
    current_date = start_date
    batch_data = [] 
    print(f"▶️ 커스텀 ID 생성 및 DB 삽입 준비 시작: {start_date} 부터 {end_date} 까지")

    while current_date <= end_date:
        
        # 1. 시간 정보 (0시 ~ 23시) 삽입
        for hour in range(24):
            custom_id = generate_custom_id(current_date, hour)
            # (ID, 날짜 객체, 시 정수)
            batch_data.append((custom_id, current_date, hour))
        
        # 2. 날짜만 있는 데이터 삽입 (record_hour = -1, ID 끝자리 99)
        custom_id_no_hour = generate_custom_id(current_date, -1)
        print(custom_id_no_hour)
    
        batch_data.append((custom_id_no_hour, current_date, -1))
        
        current_date += timedelta(days=1)
        
        # 대량 삽입 (executemany)
        if len(batch_data) >= 5000:
            if batch_data[-1][2] not in range(24) and batch_data[-1][2] != -1:
                 print(f"❌ 발견된 이상 값: {batch_data[-1]}")
            cursor.executemany(insert_sql, batch_data)
            batch_data = []
            
    # 최종 삽입
    if batch_data:
        cursor.executemany(insert_sql, batch_data)
        
    connection.commit()
    cursor.close()
    connection.close()

    total_days = (end_date - start_date).days + 1
    total_records = total_days * 25
    
    print(f"✅ 데이터 삽입 완료. 총 {total_records:,}개의 레코드 삽입.")
    
# 함수 실행
generate_and_insert_data(start_date, end_date)
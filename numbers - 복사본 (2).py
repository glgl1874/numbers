import schedule
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import json

def job():
    edge_service = Service(executable_path='C:/path_to_edgedriver/msedgedriver.exe')  # 경로 수정 필요

    # Edge 옵션 설정 (headless 모드 활성화)
    edge_options = Options()
    edge_options.add_argument('--headless')
    edge_options.add_argument('--disable-gpu')  # 필요 시 추가

    driver = webdriver.Edge(service=edge_service, options=edge_options)

    # rebuild-kc.com 로그인
    driver.get('https://rebuild-kc.com/admin')
    time.sleep(2)

    # 관리자 페이지 로그인
    username_input = driver.find_element(By.NAME, 'uid')
    password_input = driver.find_element(By.NAME, 'passwd')
    username_input.send_keys('radiant.sunny333@gmail.com')
    password_input.send_keys('Worship1027!')
    driver.find_element(By.XPATH, "//button[contains(text(), '로그인')]").click()

    time.sleep(3)  # 로그인 후 잠시 대기

    # 입력폼 데이터 페이지로 이동
    driver.get('https://rebuild-kc.com/admin/contents/form')
    time.sleep(3)

    try:
        with open('form_data.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    existing_contact_numbers = {entry['contact'] for entry in existing_data}

    # 폼 데이터 추출
    data = []
    entries = driver.find_elements(By.CSS_SELECTOR, 'ul._tbody.content')
    for entry in entries:
        contact = entry.find_element(By.CSS_SELECTOR, '.title:nth-child(6) a').text
        people = entry.find_element(By.CSS_SELECTOR, '.title:nth-child(7) a').text

        if contact not in existing_contact_numbers:
            data.append({
                'contact': contact,
                'people': people
            })

    existing_data.extend(data)

    # JSON 파일로 저장
    with open('form_data.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    driver.quit()
    print("데이터 추출 중...")

schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

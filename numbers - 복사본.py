import schedule
import time

def job():
    import json
    from selenium import webdriver
    from selenium.webdriver.edge.service import Service
    from selenium.webdriver.common.by import By

    # Edge WebDriver 경로 설정
    edge_service = Service(executable_path='C:/path_to_edgedriver/msedgedriver.exe')  # 경로 수정 필요
    driver = webdriver.Edge(service=edge_service)

    # rebuild-kc.com 로그인
    driver.get('https://rebuild-kc.com/admin')
    time.sleep(2)

    # 관리자 페이지 로그인 (필요 시 ID와 비밀번호 입력)
    username_input = driver.find_element(By.NAME, 'uid')  # ID 필드에 맞는 값을 넣어야 함
    password_input = driver.find_element(By.NAME, 'passwd')  # 비밀번호 필드에 맞는 값을 넣어야 함
    username_input.send_keys('radiant.sunny333@gmail.com')  # 실제 사용자 이름
    password_input.send_keys('Worship1027!')  # 실제 비밀번호
    driver.find_element(By.XPATH, "//button[contains(text(), '로그인')]").click()

    time.sleep(3)  # 로그인 후 잠시 대기

    # 입력폼 데이터 페이지로 이동
    driver.get('https://rebuild-kc.com/admin/contents/form')
    time.sleep(3)

    try:
        with open('form_data.json', 'r', encoding = 'utf-8') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    existing_contact_numbers = {entry['contact'] for entry in existing_data}

    # 폼 데이터 추출
    data = []
    entries = driver.find_elements(By.CSS_SELECTOR, 'ul._tbody.content')  # 각 항목의 CSS 셀렉터 확인
    for entry in entries:
        contact = entry.find_element(By.CSS_SELECTOR, '.title:nth-child(6) a').text  # 연락처
        people = entry.find_element(By.CSS_SELECTOR, '.title:nth-child(7) a').text  # 인원수

        if contact not in existing_contact_numbers:
            data.append({
                'contact': contact,
                'people': people
            })

    existing_data.extend(data)

    # JSON 파일로 저장
    with open('form_data.json', 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

    # 브라우저 종료
    driver.quit()
    # 위에서 작성한 Selenium 코드 실행
    print("데이터 추출 중...")
    # Selenium 코드 블록 삽입

(schedule.every(10).seconds.do(job))
 # minutes.do(job))  # 10분마다 실행

while True:
    schedule.run_pending()
    time.sleep(1)

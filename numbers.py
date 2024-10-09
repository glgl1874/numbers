import time
import json
import subprocess
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

# 마지막 Git 업데이트 시간을 저장하는 변수
last_git_update_time = 0

def update_git_repo():
    # 원격 저장소의 최신 커밋 가져오기
    subprocess.run(["git", "pull", "origin", "main"])
    # 변경 사항 추가 및 커밋
    subprocess.run(["git", "add", "form_data.json"])
    subprocess.run(["git", "commit", "-m", "자동 업데이트 : form_data.json 업데이트"])
    # 원격 저장소에 푸시
    subprocess.run(["git", "push", "origin", "main"])


def fetch_form_data():
    try:
        # Edge WebDriver 경로 설정
        edge_service = Service(executable_path='C:/edgedriver_win64/msedgedriver.exe')  # 경로 수정 필요
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
        driver.get('https://rebuild-kc.com/admin/contents/form/?q=YjowOw%3D%3D&pagesize=20&status=all&code=b2024090727e831837989c&pagesize=100&status=all')
        time.sleep(3)

        try:
            with open('form_data.json', 'r', encoding = 'utf-8') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []

        existing_contact_numbers = {entry['contact'] for entry in existing_data}

        # 폼 데이터 추출
        data = []
        new_data_added = False # 새로운 데이터가 추가되었는지 여부를 추적
        entries = driver.find_elements(By.CSS_SELECTOR, 'ul._tbody.content')  # 각 항목의 CSS 셀렉터 확인
        for entry in entries:
            contact = entry.find_element(By.CSS_SELECTOR, '.title:nth-child(6) a').text  # 연락처
            people = entry.find_element(By.CSS_SELECTOR, '.title:nth-child(7) a').text  # 인원수

            if contact not in existing_contact_numbers:
                data.append({
                    'contact': contact,
                    'people': people
                })
                new_data_added = True # 새로운 데이터가 추가됨

        if new_data_added:
            existing_data.extend(data)

        # JSON 파일로 저장
            with open('form_data.json', 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=4)

            print("데이터 추출 및 저장 완료")
            return True  # 새로운 데이터가 추가되었음을 반환
        else:
            print("새로운 데이터가 없습니다.")
            return False # 새로운 데이터가 없음을 반환

    except Exception as e:
        print(f"데이터 추출 중 오류 발생: {e}")
        return False  # 오류 발생 시 False 반환
    finally:
        driver.quit()


while True :
    # 위에서 작성한 Selenium 코드 실행
    print("데이터 추출 중...")
    if fetch_form_data():
        current_time = time.time()
        if current_time - last_git_update_time >= 180:
            update_git_repo()
            last_git_update_time = current_time
            print("Git 저장소가 업데이트되었습니다.")
        else :
            print("Git 업데이트 대기 중...")
    else:
        print("Git 업데이트가 필요하지 않습니다.")

    time.sleep(10)  # 5분 대기

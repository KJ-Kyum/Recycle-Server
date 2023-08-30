from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from urllib.parse import quote_plus
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import base64

# Base64를 사용하여 URL을 인코딩하는 함수
def cloak_url(url):
    """URL을 Base64로 인코딩합니다."""
    return base64.b64encode(url.encode()).decode()

# 사용자로부터 휴지 유형을 입력받습니다.
search = input("쓰레기 유형: ")

# 크롬 웹드라이버를 초기화하고 지정된 URL로 이동합니다.
driver = webdriver.Chrome()
driver.get(f'https://blisgo.com/category/{quote_plus(search)}/')

# 페이지의 '더 보기' 버튼을 위한 CSS 선택자
css_selector = "#primary > nav > span"
element = driver.find_element(By.CSS_SELECTOR, css_selector)

# '더 보기' 버튼을 최대 10번 클릭하여 콘텐츠를 더 로드합니다.
for i in range(10):
    try:
        # '더 보기' 버dld튼이 클릭 가능해질 때까지 기다린 후 클릭합니다.
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
        )
        element.click()
        time.sleep(3)  # 각 클릭 후 콘텐츠가 로드되기를 기다립니다.
    except TimeoutException:
        # '더 보기' 버튼이 지정된 시간 내에 클릭 가능하지 않으면 반복을 중단합니다.
        break

# 모든 콘텐츠가 로드될 때까지 기다립니다.
time.sleep(10)

# 모든 포스트의 셀렉터 값을 추출합니다.
post_selectors = driver.find_elements(By.CSS_SELECTOR, "[id^='post-']")

# 추출한 셀렉터 값을 출력합니다.
for post_selector in post_selectors:
    post_id = post_selector.get_attribute("id")[5:]
    print(f"Post 번호: {post_id}")

# 브라우저를 닫습니다.
driver.quit()

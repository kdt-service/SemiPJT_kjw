from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 웹 드라이버 실행
driver = webdriver.Chrome('./chromedriver.exe')  # Chrome 드라이버 경로
driver.get('https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage')

# 페이지 이동 함수
def move_to_page(page_num):
    page_input = driver.find_element_by_css_selector('#nowPage')
    page_input.clear()
    page_input.send_keys(str(page_num))
    page_input.send_keys(Keys.RETURN)

# 첫 페이지 데이터 수집
soup = BeautifulSoup(driver.page_source, 'html.parser')
# TODO: 데이터 수집 코드 구현

# 다음 페이지로 이동하여 데이터 수집
for page_num in range(2, last_page+1):
    move_to_page(page_num)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # TODO: 데이터 수집 코드 구현

# 웹 드라이버 종료
driver.quit()

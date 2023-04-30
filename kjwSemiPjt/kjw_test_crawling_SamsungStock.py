import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re


start_date = datetime(2018, 1, 2)
end_date = datetime(2023, 4, 28)

print(f"\n\n*********notStrftime날짜 start_date:  {start_date}")
print(f"\n\n*********notStrftime날짜 end_date:     {end_date}")

url = "https://www.samsungpop.com/login/sso.jsp"

links = set()

while start_date <= end_date:
    
    date_str = start_date.strftime("%Y%m%d")
    print(f"\n\n###### 날짜: {date_str}\n\n")
    
    page_url = f"{url}?regDate={date_str}"
    print(f"******page_url:   {page_url}\n\n")
    
    num_page = 1
    
    last_page = False
    
    while True:
        page_url_num = f"{page_url}&page={num_page}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        res = requests.get(page_url_num, headers=headers)
        
        if res.status_code != 200:
            print(f"https연결에 실패했습니다. page: {page_url_num}")
            continue
        soup = BeautifulSoup(res.text, "html.parser")
        #print(f"soup :   {soup} ")
        
        robot_check = soup.find('meta', attrs={'name': 'robots'})
        if robot_check and 'nofollow' in robot_check['content']:
            print('Robot검사에 걸렸습니다.')
            break
        
        article_links = soup.select(".list_news2 a.link_txt")
        print(f"\n article_links :    {article_links}")
        
        if not article_links:
            print(f"\n  CSS선택자 .list_news2 a.link_txt 에 해당하는 링크가 없습니다.  ")
            break
        
        for link in article_links:
            article_url = link["href"]
            article_res = requests.get(article_url)
            
            if article_res.status_code != 200:
                print(f"article_res의 HTTP요청이 실패했슴")
                continue
            
            article_soup = BeautifulSoup(article_res.content, "html.parser")
            date = article_soup.select_one(".info_view .txt.info")
            
            if date:
                date = re.search(r"\d{4}\.\d{2}\.\d{2}\s\d{2}:\d{2}", date.get_text())
                if date:
                    date = date.group()
                    date = datetime.strptime(date, "%Y.%m.%d %H:%M")
                    print(f"date:  {date}")
                    
            if (article_url, date):
                links.add((article_url, date))
                    

        for link, date in links:
        
            # 기사 URL 출력 (테스트용)
            print(f"\n\n☞기사링크: {link}")

            # 기사 HTML 코드 가져오기
            res = requests.get(link)

            # HTTP 요청이 성공했는지 확인
            if res.status_code != 200:
                print(f"Failed to retrieve article: {link}")
                continue

            # BeautifulSoup으로 HTML 파싱
            soup = BeautifulSoup(res.content, "html.parser")

            # 기사 제목 추출
            title = soup.select_one(".tit_view").get_text()

            # 기사 본문 추출
            contents = soup.select(".article_view p")
            content = "\n".join([c.get_text().strip() for c in contents])

            # 추출한 제목과 내용 출력
            print(f"☞기사제목: {title}")
            print(f"☞작성일자: {date_str}")
            print(f"☞Page_URL_NUM :   {page_url_num}")
            print(f"☞기사내용: \n{content}")
#            print(f"☞페이지: {num_page}") #page_url_num의 num_page를 확인하고 싶을때 출력
        
        # 마지막 페이지인지? 여부를 검사하여 다음 페이지로 이동
        
        last_page = (len(article_links) <= 14)
            # 한페이지에 15개의 기사가 있으므로 기사의 개수가 14개이하일때 마지막 페이지로 간주하도록 설정
            # IT/경제/문화 모두 한페이지에 15개의 기사가 있다.
        
        if last_page:
            print(f"\n☞ {date}의 마지막 페이지입니다. {num_page}")
            break
        num_page += 1

    # 다음 날짜로 이동
    start_date += timedelta(days=1)

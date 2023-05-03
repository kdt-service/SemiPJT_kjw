import requests
import pandas as pd
import os

# 메인 페이지 URL
main_url = 'https://kind.krx.co.kr/corpgeneral/corpList.do'

# 메인 페이지 url에 아래와 같이 요청데이터를 넣어서 post requests로
# 상장법인 목록 페이지의 팝업 창 URL 추출하는 절차를 실행한다.
main_params = {
    'method': 'loadInitPage'
}
main_response = requests.post(main_url, data=main_params)
#HTTP약속에서 클라이언트가 서버에게 요청을 보내는 방식에는 크게
#두가지가 있는데, 하나는 우리가 배운 get방식이고, 하나가 post방식
#post는 서버에게 데이터를 전달할때 사용하는 방식
#get은 서버에게 데이터를 요청하는 방식이다.
#post는 데이터를 요청 url뒤 ?에 연달아 붙여서 전송하는 get과 달리
#요청헤더와 메시지 본문에 데이터를 담아서 전송한다. 
#보안성이 높은 데이터(예: 로그인 정보, 결제 정보 등)를 전송할 때 
#사용하며, 데이터의 크기에 제한이 없기 때문에 GET 방식보다 
#더 많은 양의 데이터를 전송할 수 있다
#post방식으로 http전송할때는 요청header와 요청data가 필요하다.
#요청data는 딕셔너리형태로 위의 main_params처럼 넣어준다.
#요청header는 필수적인 것이 아니다. 요청header를 생략하더라도
#requests모듈이 필요정보를 자동으로 추가해준다.
#requests 모듈에서는 기본적으로 User-Agent와 Accept-Encoding 
#정보가 포함된 요청 헤더를 자동으로 생성하여 전송해준다.
print(f'\n\n  main_response: {main_response.status_code}\n\n')

popup_url = main_response.url
#위에서 .url은 response객체의 속성이다.
#post방식으로 요청하여 응답받은 main_response에서
#' 팝업 창 url '을 ' 추출 '하기 위해서 .url속성을 사용하였다.
#.url은 요청에 대한 최종 url을 '문자열'로 반환하는 속성이다.

print(f'\n\n******이것이 popup_url 입니다. {popup_url}\n\n')
#위와같이 출력해보면 popup_url 주소는 
#https://kind.krx.co.kr/corpgeneral/corpList.do
#위 주소를 직접 브라우저에 입력하면 KRX가 get방식으로 직접 접근을 
#막아놓았다는 것을 알 수 있다. ? 뒤에 요청data를 직접입력해도
#계속 안내멘트 사이트만 뜨는 것이다.
#poost requests를 통해 정보를 받기 위해서 아래와 같은 포맷으로
#요청을 구성해야 한다.  response = requests.post(url, 요청데이터)
#상장법인목록을 다운로드받기 위한 POST requests의 요청데이터는 상장법인목록
#https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage
#사이트의 F12 개발자도구를 열어놓고 상장법인목록을 한꺼번에 
#다운로드 받을 '검색'아이콘옆에 있는 '엑셀'아이콘을 클릭했을때
#Network탭에서 생성되는 corpList.do 이름의 Network탭 Payload에서
#요청데이터를 확인할 수 있다. 

#팝업 창 URL에서 페이지 이동을 위한 데이터 추출
popup_response = requests.get(popup_url)
#popup_url 즉, https://kind.krx.co.kr/corpgeneral/corpList.do에서
#상장종목목록을 가져와야 되는데, 브라우저에서 들어가보면 정보가 없다.
#그래서 팝업 창을 열기 위해 GET 요청을 보내는 이유는, 
#서버에서는 팝업 창을 열기 위한 HTML 페이지를 반환하기 때문. 
#이 HTML 페이지는 브라우저에서 실행되어야 하므로, 
#GET 요청을 이용하여 HTML 페이지를 받아온 뒤, 
#이를 이용하여 팝업 창을 띄운다.
#따라서, main_response 객체에서 추출한 팝업 창 URL을 
#이용하여 GET 요청을 보내는 것
#그리고, post가 아닌 get으로 requests를 보내는 이유는 
#https://kind.krx.co.kr/corpgeneral/corpList.do 사이트에서
#F12를 클릭하여 '개발자도구'를 열고 Network탭으로 들어간 뒤에
#페이지고침을 클릭해서 Network 정보를 확인한뒤 header탭으로 들어가
#General을 보면 '요청메서드(requests method)'가 get 으로
#되어 있기 때문이다. 이제 .status_code를 통해 결과값이 200인지 확인
#print(popup_response.status_code)  # 결과값이 200 이 나올 것이다.

popup_params = {
    'method': 'download',
    'searchType': '13',
    'fiscalYearEnd': 'all',
    'comAbbrvTmp': '',
    'location': 'all',
    'marketType': 'ALL',
    'pageIndex': 1,
    'pageSize': 3000,
}

#위 코드가 바로 POST requests에서 사용할 요청header와 
#요청data중에서 ' 요청data '에 해당한다. 
#이름을 popup_params로 했다.
#위의 요청데이터의 키와 값은 상장법인목록 사이트
#https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage
#사이트의 F12 눌러서 개발자도구를 열어놓고 '검색'아이콘옆에 있는
#상장법인목록을 한꺼번에 다운로드 받을  '엑셀' 아이콘을 클릭했을때
#Network탭에서 생성되는 corpList.do 이름의 Network탭 Payload에서
#요청데이터를 확인할 수 있다. 
#corpList.do가 여러개 있는데, 반드시 '엑셀'아이콘을 눌렀을때 생성되는
#corpList.do이름의 network탭 Payload를 확인해야 된다.
#그리고, 브라우저는 반드시 chrome을 써라 웨일같은 브라우저에는
#payload가 표시되지 않을 수 있다.

# 숫자(종목코드) 출력 형식을 변경하는 코드인데, 아래 두 코드는 종목코드의 숫자앞 0을 유지시키는데 전혀 쓸모가 없었다.
#pd.option.display.float_format = '{:.of}'.format
#pd.set_option('float_format', '{:2f}'.format)


# 첫 페이지부터 마지막 페이지까지 데이터 수집
results = pd.DataFrame()
while True:
    # 페이지 이동을 위한 데이터를 이용하여 POST 요청 보내기
    popup_response = requests.post(popup_url, data=popup_params)
    #print(f'\n 출력 popup_response는 \n {popup_response.text}\n')
    temp_df = pd.read_html(popup_response.text, converters={'종목코드': str})[0]
    #converters={'종목코드': str}을 read_html()메소드의 매개변수로
    #추가했다. 종목코드에서 숫자앞의 0이 유지될 수 있도록 
    #추가한 것이다. 숫자로만 이뤄진 종목코드 열을
    #이렇게 판다스 데이터프레임에서 '문자열'로 인식할 수 있도록
    #html문서안에서 작업을 미리 해주어야 한다.
    #html문서안에서 작업을 안해주고 판다스 pandas read메소드로
    #읽어들인 후에 종목코드 열을 문자열로 처리해도 이미 읽어드릴때
    #숫자열로 읽어들이면서 숫자앞의 0을 무시해버렸기 때문에
    #이미 000100은 100이 되어 있는 상태에서 문자열이 되는것이다
    #따라서, html문안에서 converters매개변수로 바꿔주고 pandas로 
    #읽어야 된다. pandas데이터프레임에서 문자열로 된 상태로 하더라도
    #to-csv()메소드를 통해 csv파일을 만들때 to_csv()메소드가
    #숫자로만 되어 있는 종목코드 열을 '문자열'로 지정되어 있슴에도
    #불구하고 '숫자'로 추론하여 숫자앞의 0을 무시하고 000100을
    #다시 100으로 출력해버린다. 이것은 df문을 출력해보고,
    #csv파일을 출력해서 비교해 보면 df데이터프레임문에서는 문자열인데
    #csv파일의 종목코드열에서는 숫자앞의 0이 무시되어 숫자열로
    #처리되어 있는 것을 확인할 수 있다.
    #to-csv파일로 출력할때 숫자앞의 0이 유지되도록 하는 방법은
    #아직 찾질 못했다. 아래와 같이 써서
    #temp_df['종목코드'] = '"' + temp_df['종목코드'] + '"'
    #쌍따옴표안에 숫자를 넣고 문자열로 인식시켜서 숫자앞의 0이
    #유지되도로 하여 csv로 출력하고,
    #csv화일의 종목코드 열을 읽어들일때는 .strip('"') 메소드를
    #사용해서 쌍따옴표를 없애는 방법밖에는 찾지 못했다.
    #print(f'\n 출력 temp_df는 \n {temp_df}\n')
    temp_df['종목코드'] = temp_df['종목코드'].astype(str) # 쑷자앞에 0을 유지시키기 위해서 타입을 str(문자열)로 변경시킨다.
    #temp_df['종목코드'] = '  temp_df['종목코드']  '
    #temp_df['종목코드'] = '"' + temp_df['종목코드'] + '"'
    #temp_df['종목코드'] = temp_df['종목코드'].apply(lambda x: f'"{x:0>6}"')
    results = pd.concat([results, temp_df], ignore_index=True)
    #print(f'\n 확인을 위한 출력 response.text :\n{results}')
    # 다음 페이지로 이동하기 위해 pageIndex 값을 1 증가시킴
    popup_params['pageIndex'] += 1
    
    # 마지막 페이지인지 확인
    if len(temp_df) < popup_params['pageSize']:
        break

#결과데이터를 csv화일로 출력
#print(f'\n 최종확인 출력 results 최종출력은 \n {results}\n')
#file_path = os.path.join(os.getcwd(), 'CrawlStockInfo','stockCodeList_test_029.csv')
#results['종목코드'] = results['종목코드'].astype(str)
#results.to_csv(file_path, index=False)

#결과데이터를 txt화일로 출력
#text_file_path = os.path.join(os.getcwd(), 'CrawlStockInfo','stockCodeList_test_001.txt')
#with open(text_file_path, 'w') as f:
#    f.write(results.to_string(index=False))

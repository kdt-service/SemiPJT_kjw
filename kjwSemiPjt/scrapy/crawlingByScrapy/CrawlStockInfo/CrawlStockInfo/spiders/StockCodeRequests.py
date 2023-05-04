import requests
import pandas as pd
import scrapy
import os
import csv
import io
import datetime

print(f'\n\n######## 시작 #########\n\n')
    
main_url = 'https://kind.krx.co.kr/corpgeneral/corpList.do'   # ?method=loadInitPage'
main_params ={
    'method' : 'loadInitPage'
}   #main_params를 요청데이터에 넣으면 상장법인목록 
main_response = requests.post(main_url, data=main_params)
popup_url = main_response.url  #.url을 통해 요청http에서 보내준 팝업창 url을 추출할 수 있다.
print(f'☞확인용출력_popup_url주소는 {popup_url}\n\n') #https://kind.krx.co.kr/corpgeneral/corpList.do 인 것을 알 수 있다.
popup_response_1 = requests.get(popup_url)  
print(f'☞확인용출력 popup_response_1.status_code: {popup_response_1.status_code}\n\n')  #200인지? 확인
popup_params ={
    'method':'download',
    'searchType':'all',
    'fiscalYearEnd':'',
    'comAbbrvTmp':'',
    'location': 'all',
    'marketType':'ALL',
    'pageIndex':1,
    'pageSize': 3000
}
popup_response_2 = requests.post(popup_url, data=popup_params)
df_code = pd.read_html(popup_response_2.text, converters={'종목코드': str})[0]
print(f'☞확인용출력  df_code.head(2): \n\n{df_code.head(2)}\n\n')
df_code['종목코드'] = '"' + df_code['종목코드'] + '"'  #종목코드열의 숫자앞에 0이 to_csv()함수에서 처리될때 무시되지 않도록 구문추가
time_stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
file_name =  f'stockcode_{time_stamp}.csv'
file_path = os.path.join(os.getcwd(), 'FileHouseStock', file_name)
df_code.to_csv(file_path, index=False)  #DataFrame의 인덱스를 csv파일에 포함시키지 않으려고 False로 설정
print(f'######## 성공 #########\n\n')
import requests
import pandas as pd
import os

# 메인 페이지 URL
main_url = 'https://kind.krx.co.kr/corpgeneral/corpList.do'

# 메인 페이지에 POST 요청을 보내서 팝업 창 URL 추출
main_params = {
    'method': 'loadInitPage'
}
main_response = requests.post(main_url, data=main_params)
popup_url = main_response.url

# 팝업 창 URL에서 페이지 이동을 위한 데이터 추출
popup_response = requests.get(popup_url)
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
    #converters={'종목코드': str}을 read_html()메소드의 매개변수로 추가했다. 종목코드에서 숫자앞의 0이 유지될 수 있도록 추가한 것이다.
    print(f'\n 출력 temp_df는 \n {temp_df}\n')
    temp_df['종목코드'] = temp_df['종목코드'].astype(str) # 쑷자앞에 0을 유지시키기 위해서 타입을 str(문자열)로 변경시킨다.
    #temp_df['종목코드'] = '  temp_df['종목코드']  '
    temp_df['종목코드'] = '"' + temp_df['종목코드'] + '"'
    #temp_df['종목코드'] = temp_df['종목코드'].apply(lambda x: f'"{x:0>6}"')
    results = pd.concat([results, temp_df], ignore_index=True)
    #print(f'\n 확인을 위한 출력 response.text :\n{results}')
    # 다음 페이지로 이동하기 위해 pageIndex 값을 1 증가시킴
    popup_params['pageIndex'] += 1
    
    # 마지막 페이지인지 확인
    if len(temp_df) < popup_params['pageSize']:
        break

#결과데이터를 csv화일로 출력
print(f'\n 최종확인 출력 results 최종출력은 \n {results}\n')
file_path = os.path.join(os.getcwd(), 'CrawlStockInfo','stockCodeList_test_029.csv')
#results['종목코드'] = results['종목코드'].astype(str)
results.to_csv(file_path, index=False)

returns = pd.read_csv(file_path)
while True:
    ac = returns['종목코드'][0].strip('"')
    print(ac)
    break

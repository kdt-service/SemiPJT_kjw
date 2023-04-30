import requests as rq

# KOSPI 종목코드 조회
url_kospi = "http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13"
rs_kospi = rq.get(url_kospi)
rs_kospi.status_code
print(rs_kospi.status_code)

rows_kospi = rs_kospi.text.split('\n')
for row_kospi in rows_kospi:
    if '유가증권시장상장법인' in row_kospi:
        code_kospi = row_kospi.split('\t')[1]
        print(code_kospi)

# KOSDAQ 종목코드 조회
url_kosdaq = "http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=04"
rs_kosdaq = rq.get(url_kosdaq)
rs_kosdaq.status_code
print(rs_kosdaq.status_code)

rows_kosdaq = rs_kosdaq.text.split('\n')
for row_kosdaq in rows_kosdaq:
    if '코스닥시장상장법인' in row_kosdaq:
        code_kosdaq = row_kosdaq.split('\t')[1]
        print(code_kosdaq)
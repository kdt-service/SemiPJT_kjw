import numpy as np 
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
train_df = pd.read_csv("./semiPjt_train.csv")
test_df = pd.read_csv("./semiPjt_test.csv")
# 입력변수 데이터 생성
df = pd.read_csv('semiPjt_train.csv')
X = df[['환율', '금리', '배당수익율', '당기순이익율', 'PER', '핵심키워드종합순위']]
# 종속변수 라벨링
y = y.map({'선정': 1, '비선정': 0})
# 입력변수 조건 충족하는 종목 전처리 필터링
X_selected = X[(X['환율'] >= 1250) & (X['금리'] <= 2.0%) & (X['배당수익율'] >= 4%) & (X['당기순이익율'] >= 10%) & (X['PER'] <= 12)& (X['핵심키워드종합순위'] <= 3)]
# Random Forest 모델 훈련
rf = RandomForestClassifier(n_estimators=100)
rf.fit(X_selected, y)

#정확도 계산
rf.score(X_selected, y)

# 테스트 데이터에 대한 종속변수(선정/비선정) 예측
new_X = pd.read_csv('semiPjt_test.csv')
y_pred = rf.predict(new_X)

# csv로 출력
submission = pd.DataFrame({
        "종목명": test_df["종목명"],
        "선정/비선정": y_pred
    })
submission.to_csv('selection.csv', index=False)

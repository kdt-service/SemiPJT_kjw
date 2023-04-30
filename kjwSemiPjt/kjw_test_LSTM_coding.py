import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt

# 데이터 불러오기
end_date = pd.Timestamp.now()
start_date = end_date - pd.Timedelta(days=1000)
df = pd.read_csv('주식데이터.csv', encoding='cp949', index_col='날짜', parse_dates=True)
df = df.loc[(df.index >= start_date) & (df.index <= end_date)]

# 입력 데이터 정규화
scaler = MinMaxScaler()
scaled_df = scaler.fit_transform(df)

# 입력 데이터와 종속변수 분리
X = []
Y = []
for i in range(60, len(scaled_df)):
    X.append(scaled_df[i-60:i, 0:6])
    Y.append(scaled_df[i, 0])
X = np.array(X)
Y = np.array(Y)

# 훈련 데이터와 검증 데이터 분리
train_size = int(len(X)*0.8)
X_train, X_val = X[:train_size], X[train_size:]
Y_train, Y_val = Y[:train_size], Y[train_size:]

# LSTM 모델 생성
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(LSTM(units=50))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')

# 모델 학습
model.fit(X_train, Y_train, epochs=100, batch_size=32, validation_data=(X_val, Y_val), verbose=2)

# 모델 예측
inputs = df.values
scaled_inputs = scaler.transform(inputs)
X_test = []
for i in range(60, len(scaled_inputs)):
    X_test.append(scaled_inputs[i-60:i, 0:6])
X_test = np.array(X_test)
predicted_prices = model.predict(X_test)
predicted_prices = scaler.inverse_transform(predicted_prices)

# 예측 결과 출력
print(predicted_prices)




# 예측 결과 그래프 출력
plt.figure(figsize=(16,8))
plt.plot(df.index[-len(predicted_prices):],predicted_prices,label='Predictions')
plt.plot(df.index[-len(predicted_prices):],df['종가'][-len(predicted_prices):],label='Actual')
plt.legend(loc='upper left')
plt.show()
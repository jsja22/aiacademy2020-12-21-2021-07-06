import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model,Sequential
from tensorflow.keras.layers import Dense, Input, LSTM, Dropout, Conv1D, Flatten, MaxPooling1D, LeakyReLU , GRU , BatchNormalization
from sklearn.metrics import mean_squared_error, r2_score
from tensorflow.keras.layers import concatenate, Concatenate
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint ,ReduceLROnPlateau
from tensorflow.keras.models import load_model
#함수정의
def split_data(seq, size):
    aaa = []
    for i in range(len(seq)-size+1):
        subset = seq[i : (i+size)]
        aaa.append([item for item in subset])
    print(type(aaa))
    return np.array(aaa)

def RMSE(y_test, y_predict):
    return np.sqrt(mean_squared_error(y_test, y_predict))

# 1. 데이터
samsung = np.load('C:/data/npy/samsung_2.npy')
kodex = np.load('C:/data/npy/kodex.npy')

print(samsung.shape) #(1085, 6)
print(kodex.shape) #(1085, 6)
print(samsung)
print(kodex)

x1 = samsung
x2 = kodex
y= x1[:,0]

print(x1)
print(x2)

print(x1.shape, x2.shape) #(1085, 6) (1085, 6)
print(y.shape) #(1085,)

#전처리
scaler1 = MinMaxScaler()
scaler1.fit(x1)
x1 = scaler1.transform(x1)

scaler2 = MinMaxScaler()
scaler2.fit(x2)
x2 = scaler2.transform(x2)

print(x1)
print(x2)
################################전처리 완료
size1 = 12
x1 = split_data(x1, size1)
x2 = split_data(x2, size1)

x1 = x1[:-2,:,:]
x2 = x2[:-2,:,:]

size2 =  2

y= split_data(y,size2)
y= y[size1:,:]

x1_pred = x1[-20:,:,:]
x2_pred = x2[-20:,:,:]
print(x1.shape) #(1064, 20, 6)
print(x2.shape) #(1064, 20, 6)
print(y.shape)  #(1064, 2)


#train test 분류
x1_train, x1_test, x2_train, x2_test, y_train, y_test = train_test_split(x1, x2, y, train_size=0.8, shuffle=True, random_state=99)
x1_train, x1_val, x2_train, x2_val, y_train, y_val = train_test_split(x1_train, x2_train, y_train, train_size=0.8, shuffle = True,random_state=99)

#leakrelu 썻는데 load에서 불러와지지 않는다 이유 해결해보기!

model = load_model('C:/data/h5/samsung_kodex.h5')

loss, mae = model.evaluate([x1_test,x2_test], y_test, batch_size=32)
y_predict = model.predict([x1_test, x2_test])
r2 = r2_score(y_test, y_predict)
print("loss, mae : ", loss, mae)
print("RMSE : ", RMSE(y_test, y_predict))
print("R2 : ", r2)

y_predict = model.predict([x1_pred,x2_pred])
print(y_predict)
print(y_predict.shape) #(20, 2)

for i in range(len(y_predict)):
    print("다 다음날의 실제 시가",y[-(y_predict.shape[0])+i,-1],"다 다음날의 예측 시가", y_predict[i][1] )


plt.figure(figsize=(12, 9))
plt.plot(np.asarray(y)[-20:,1], label='actual')
plt.plot(y_predict[:,1], label='prediction')
plt.legend()
plt.grid()
plt.show()

print("1/18일 예측 시가는?", y_predict[-1,0],"1/19일 예측 시가는?", y_predict[-1,1])

#size 6 , epochs 80
#loss, mae :  10918207.0 1807.4273681640625
#RMSE :  3304.271139318148
#R2 :  0.8926200914040961

#1/19일 예측 시가는? 91997.305


#size 12 , epochs 80
#loss, mae :  6018545.0 1605.6842041015625
#RMSE :  2453.2722663875584
#R2 :  0.9026400627530704

#1/19일 예측 시가는? 90057.17

#size 20, BatchNormalization 적용
#loss, mae :  1014967.875 786.8383178710938
#RMSE :  1007.4564933459484
#R2 :  0.9824107521423031

#1/18일 예측 시가는? 92615.15 1/19일 예측 시가는? 92722.27

#loss, mae :  1722627.625 1036.841064453125
#RMSE :  1312.4891897971959
#R2 :  0.9701306354393802
#1/18일 예측 시가는? 90683.5 1/19일 예측 시가는? 90760.68

#loss, mae :  1369425.75 943.8727416992188
#RMSE :  1170.2246588012915
#R2 :  0.9778459933647354
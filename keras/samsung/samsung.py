import numpy as np
import pandas as pd
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from sklearn.metrics import mean_squared_error,r2_score
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
#함수정의
def split_x(data,size):
    a = []
    for i in range(data.shape[0] - size + 1):
        a.append(np.array(data.iloc[i:(i+size), 0:len(data.columns)]))
    return  np.array(a)

dataset = pd.read_csv('C:/data/csv/samsung.csv', index_col=0, header=0, encoding='cp949')

dataset['시가'] = dataset.loc[:,['시가']].apply(lambda x: x.str.replace(',', '').astype(float), axis=1)
dataset['고가'] = dataset.loc[:,['고가']].apply(lambda x: x.str.replace(',', '').astype(float), axis=1)
dataset['저가'] = dataset.loc[:,['저가']].apply(lambda x: x.str.replace(',', '').astype(float), axis=1)
dataset['종가'] = dataset.loc[:,['종가']].apply(lambda x: x.str.replace(',', '').astype(float), axis=1)
dataset['거래량'] = dataset.loc[:,['거래량']].apply(lambda x: x.str.replace(',', '').astype(float), axis=1)
dataset['금액(백만)'] = dataset.loc[:,['금액(백만)']].apply(lambda x: x.str.replace(',', '').astype(float), axis=1)
dataset['개인'] = dataset.loc[:,['개인']].apply(lambda x: x.str.replace(',', '').astype(float), axis=1)
dataset['기관'] = dataset.loc[:,['기관']].apply(lambda x: x.str.replace(',', '').astype(float), axis=1)
dataset['외인(수량)'] = dataset.loc[:,['외인(수량)']].apply(lambda x: x.str.replace(',', '').astype(float), axis=1)
dataset['외국계'] = dataset.loc[:,['외국계']].apply(lambda x: x.str.replace(',', '').astype(float), axis=1)
dataset['프로그램'] = dataset.loc[:,['프로그램']].apply(lambda x: x.str.replace(',', '').astype(float), axis=1)

print(type(dataset.iloc[0, 1]))   #<class 'numpy.float64'>

dataset = dataset.iloc[:662, :][::-1]

print(dataset.shape)      # (662, 14)
print(dataset)

dataset = dataset.sort_values(by='일자' ,ascending=True) 
print(dataset)

# #결측값 제거
# datasets_1 = dataset.iloc[:662,:]
# datasets_2 = dataset.iloc[665:,:]

# dataset = pd.concat([datasets_1,datasets_2],ignore_index=True)

# print(dataset.shape)      # (662, 14)
# print(dataset)


x = dataset.drop(['종가'], axis=1)
x = dataset.iloc[:,:5]
y = dataset['종가']

print(x) #[662 rows x 5 columns]
print(y)  

print(x.shape)         # (662, 5)
print(y.shape)         # (662,)


size = 20
x_data = split_x(x,size)
y_target = y[size:]

print(x_data.shape)  #(643, 20, 5)
print(y_target.shape)  #(642,)

#train, test 분류
x_train, x_test, y_train, y_test = train_test_split(x_data[:-1], y_target, test_size=0.2, shuffle=False)
#x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, train_size=0.8, shuffle=True)

x_train = x_train.reshape(x_train.shape[0], x_train.shape[1]*x_train.shape[2])
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1]*x_test.shape[2])
#x_data = x_data.reshape(x_test.shape[0], x_test.shape[1],x_train.shape[2])

print(x_train.shape)
print(x_test.shape)
#전처리
scaler = MinMaxScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

x_data1 = x_data.reshape(x_data.shape[0], x_data.shape[1]*x_data.shape[2])
x_data2 = scaler.transform(x_data1)
x_data = x_data2.reshape(x_data.shape[0],x_data.shape[1],x_data.shape[2])

x_train = x_train.reshape(x_train.shape[0], x_data.shape[1], x_data.shape[2])
x_test = x_test.reshape(x_test.shape[0], x_data.shape[1], x_data.shape[2])

np.save('C:/data/npy/samsung_x_train.npy', arr=x_train)
np.save('C:/data/npy/samsung_x_test.npy', arr=x_test)
np.save('C:/data/npy/samsung_y_train.npy', arr=y_train)
np.save('C:/data/npy/samsung_y_test.npy', arr=y_test)
np.save('C:/data/npy/samsung_x_data.npy', arr=x_data)

# 모델
model = Sequential()

model.add(LSTM(256, activation='relu', input_shape=(x_train.shape[1],x_train.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(256, activation='relu'))
model.add(Dense(128, activation='relu'))
model.add(Dense(1))

model.summary()

model.compile(loss='mse', optimizer='adam')
modelpath = 'C:/data/modelcheckpoint/samsung_stock.hdf5'
es = EarlyStopping(monitor='val_loss', patience=50, mode='auto')
cp = ModelCheckpoint(filepath=modelpath, monitor='val_loss', save_best_only=True, mode='auto')
model.fit(x_train, y_train, epochs=2000, batch_size=32, validation_split=0.2, verbose=1, callbacks=[es,cp])

model.save('C:/data/h5/samsung_stock.h5')

loss = model.evaluate(x_test, y_test)
print('loss :', loss)

y_predict = model.predict(x_test)

def RMSE(y_test, y_predict) : 
    return np.sqrt(mean_squared_error(y_test, y_predict))  
print("RMSE :" , RMSE(y_test, y_predict))

r2 = r2_score(y_test, y_predict)
print("R2 : ", r2 )


y_pred1 = x_data[-1].reshape(-1,x_train.shape[1],x_train.shape[2])
value = model.predict(y_pred1)
print('종가= ', value)

#loss : 8253369.0
#RMSE : 2872.8672350433526
#MSE : 8253366.150185637
#R2 : 0.8954794794211476

#종가=  [[85627.89]]
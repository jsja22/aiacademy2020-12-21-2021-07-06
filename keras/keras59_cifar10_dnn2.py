##다차원 댄스 모델?
#(n,32,32,3) ->(n,10)

import numpy as np
import matplotlib.pyplot as plt

from tensorflow.keras.datasets import cifar10
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Conv2D,MaxPooling2D,Flatten,LSTM,Dropout
from tensorflow.keras.callbacks import EarlyStopping


es = EarlyStopping(monitor='loss',patience = 10)
(x_train,y_train),(x_test,y_test) = cifar10.load_data()
#  (50000, 32, 32, 3) (50000, 1)
#  (10000, 32, 32, 3) (10000, 1)

x_train = x_train.reshape(-1,32,32,3).astype('float32')/255
x_test= x_test.reshape(-1,32,32,3).astype('float32')/255

onehot = OneHotEncoder()
y_train = onehot.fit_transform(y_train.reshape(-1,1)).toarray()
y_test = onehot.transform(y_test.reshape(-1,1)).toarray()

print(y_test.shape)
model = Sequential()
model.add(Dense(128,activation='relu',input_shape=(32,32,3)))
model.add(Dropout(0.4))
model.add(Dense(128,activation='relu'))
model.add(Flatten()) 
model.add(Dense(64,activation='relu'))
model.add(Dense(32,activation='relu'))
model.add(Dense(10,activation='softmax')) #(None,10)  

model.summary()

model.compile(loss ='categorical_crossentropy',optimizer='adam',metrics = ['accuracy'])
model.fit(x_train,y_train,validation_split=0.2,epochs=200,callbacks=[es],batch_size=16,verbose=1)

loss = model.evaluate(x_test,y_test,batch_size=16)
y_predict = model.predict(x_test)
y_test = np.argmax(y_test,axis=-1)
y_predict = np.argmax(y_predict,axis=-1)

import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D,MaxPooling2D,Dense,Flatten,Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.datasets import mnist

(x_train,y_train),(x_test,y_test) = mnist.load_data()
x_train = x_train.reshape(60000,28,28,1).astype('float32')/255.
x_test = x_test.reshape(-1,28,28,1)/255.

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

model = Sequential()
model.add(Conv2D(filters = 256,kernel_size = (2,2),padding='same',strides = 1,input_shape=(28,28,1)))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.2))
model.add(Conv2D(256,kernel_size=(2,2)))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(64,activation='relu'))
model.add(Dense(32,activation='relu'))
model.add(Dense(16,activation='relu'))
model.add(Dense(10,activation='softmax'))

model.save('C:/data/h5/k52_1_model1.h5')  #훈련전에는 훈련값이 안들어가기 때문에 weight를 save하지 않음

model.compile(loss = 'categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
modelpath = 'C:/data/modelcheckpoint/k52_1_mnist_{epoch:02d}-{val_loss:.4f}.hdf5'
cp = ModelCheckpoint(filepath = modelpath, monitor='val_loss',save_best_only = True, mode = 'auto')
es = EarlyStopping(monitor='val_loss',patience=10)
hist = model.fit(x_train,y_train,validation_split = 0.2,epochs=50,verbose=1,batch_size=16,callbacks=[es,cp])


model.save('C:/data/h5/k52_1_model2.h5')  #weight까지 저장
model.save_weights('C:/data/h5/k52_1_weight.h5')

result = model.evaluate(x_test,y_test,batch_size=16)
print('loss : ',result[0])
print('accuracy : ',result[1])






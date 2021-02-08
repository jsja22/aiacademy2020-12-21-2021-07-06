#epochs 100
# validation_split, callbacks 적용
#es 5 적용
#reduce_lr 3적용
#cp 적용
#modelcheckpoihnt 폴더에 hdf5 파일저장

import numpy as np
from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.layers import Dense ,Dropout, Input,Conv2D, Flatten, MaxPooling2D 
from sklearn.datasets import load_wine
from tensorflow.keras.optimizers import Adam, Adadelta, Adamax, Adagrad
from tensorflow.keras.optimizers import RMSprop, SGD, Nadam
from tensorflow.keras.layers import LeakyReLU
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

dataset = load_wine()
x= dataset.data
y= dataset.target

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,shuffle=True  ,random_state=66)

scalar = MinMaxScaler()
scalar.fit(x_train)
x_train=scalar.transform(x_train)
x_test = scalar.transform(x_test)

from tensorflow.keras.utils import to_categorical

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

#2. 모델
def build_model(drop=0.5,optimizer='adam',activation='relu',lr=0.001,nodes=64):
    Inputs = Input(shape=(13,),name='input')
    x = Dense(512, activation='relu',name='hiddne1')(Inputs)
    x = Dropout(drop)(x)
    x = Dense(256, activation='relu',name='hiddne2')(x)
    x = Dropout(drop)(x)
    x = Dense(128, activation='relu',name='hiddne3')(x)
    x = Dropout(drop)(x)
    x = Dense(32, activation='relu',name='hiddne4')(x)
    x = Dropout(drop)(x)
    outputs = Dense(3,activation='softmax' ,name='outputs')(x)

    model = Model(inputs=Inputs, outputs=outputs)
    model.compile(optimizer=optimizer, metrics=['acc'],loss='categorical_crossentropy')

    return model

def create_hyperparameters():
    batchs = [8,16,32,64,128]
    optimizers = ['rmsprop','adam','adadelta','SGD']
    nodes =[32,64,128]
    lr=[0.1, 0.01, 0.001]
    dropout = [0.2,0.3,0.5]
    activation = ['tanh', 'relu', "selu", "sigmoid", LeakyReLU()] #{'optimizer': 'adam', 'nodes': 32, 'lr': 0.01, 'drop': 0.3, 'batch_size': 64, 'activation': 'sigmoid'}
    return {"batch_size" : batchs, "optimizer":optimizers, "drop":dropout, "activation":activation, "lr":lr, "nodes":nodes}

hyperparameters = create_hyperparameters()
model2 = build_model()

from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
model2 = KerasClassifier(build_fn=build_model, verbose=1)   #머신러닝이 keras보다 먼저 나왔기에 무언가 알아먹게 해줘야하는데 그것이 이두줄로 정의된다.
#keras모델을 래핑을 해야 그리드서치나 랜덤서치가 알아먹는다

from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from tensorflow.keras.callbacks import EarlyStopping,ModelCheckpoint, TensorBoard, ReduceLROnPlateau
reduce_lr = ReduceLROnPlateau(monitor='val_loss',patience=3,factor=0.5,verbose=1)  
es = EarlyStopping(monitor='val_loss', patience=5, mode='auto')
#modelpath = ('C:/data/modelcheckpoint/keras61_4_epochs-{epoch:02d}-{val_loss:.4f}.hdf5')
#cp = ModelCheckpoint(modelpath, monitor='val_loss', save_best_only=True, mode='auto')
search = RandomizedSearchCV(model2,hyperparameters,cv=3 )
search.fit(x_train,y_train, verbose=1,validation_split=0.2, epochs=100,callbacks=[reduce_lr,es])
print(search.best_estimator_)  
print(search.best_params_) 
print(search.best_score_)  
acc = search.score(x_test,y_test)
print("최종 스코어 :", acc) 

# <tensorflow.python.keras.wrappers.scikit_learn.KerasClassifier object at 0x000001B58695EAC0>
# {'optimizer': 'adam', 'nodes': 128, 'lr': 0.01, 'drop': 0.2, 'batch_size': 16, 'activation': 'tanh'}
# 0.9790189067522684
# 3/3 [==============================] - 0s 2ms/step - loss: 0.0825 - acc: 0.9722
# 최종 스코어 : 0.9722222089767456
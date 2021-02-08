#61카피해서
#model.cv_result를 붙여서 완성

import numpy as np
from tensorflow.keras.models import Sequential,Model
from tensorflow.keras.layers import Dense ,Dropout, Input
from tensorflow.keras.datasets import mnist

(x_train,y_train), (x_test,y_test) = mnist.load_data()
print(x_test.shape)

#1. 데이터 / 전처리

from tensorflow.keras.utils import to_categorical
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

x_train = x_train.reshape(60000,28*28).astype('float32')/255.
x_test = x_test.reshape(10000,28*28).astype('float32')/255.

#2. 모델
def build_model(drop=0.5,optimizer='adam'):
    Inputs = Input(shape=(28*28,),name='input')
    x = Dense(512, activation='relu',name='hiddne1')(Inputs)
    x = Dropout(drop)(x)
    x = Dense(256, activation='relu',name='hiddne2')(x)
    x = Dropout(drop)(x)
    x = Dense(128, activation='relu',name='hiddne3')(x)
    x = Dropout(drop)(x)
    outputs = Dense(10, activation='softmax',name='outputs')(x)

    model = Model(inputs=Inputs, outputs=outputs)
    model.compile(optimizer=optimizer, metrics=['acc'],loss='categorical_crossentropy')

    return model

def create_hyperparameters():
    batchs = [8,16,32,64,128]
    optimizers = ['rmsprop','adam','adadelta']
    dropout = [0.1,0.2,0.3]
    return {"batch_size" : batchs, "optimizer":optimizers, "drop":dropout}

hyperparameters = create_hyperparameters()
model2 = build_model()

from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
model2 = KerasClassifier(build_fn=build_model, verbose=1)   #머신러닝이 keras보다 먼저 나왔기에 무언가 알아먹게 해줘야하는데 그것이 이두줄로 정의된다.
#keras모델을 래핑을 해야 그리드서치나 랜덤서치가 알아먹는다

from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
search = RandomizedSearchCV(model2,hyperparameters,cv=3 )

search.fit(x_train,y_train, verbose=1)
print(search.best_estimator_)   #<tensorflow.python.keras.wrappers.scikit_learn.KerasClassifier object at 0x000001ED0BB8E430>
print(search.best_params_) #내가 선택한 파라미터 배피사이즈, 드랍아웃, 옵티마이저 중 가장 좋은것 #{'optimizer': 'adam', 'drop': 0.1, 'batch_size': 30}
print(search.best_score_)  #0.9574999809265137
acc = search.score(x_test,y_test)
print("최종 스코어 :", acc) #최종 스코어 : 0.970300018787384
print(search.cv_results_) #각종 cv 결과값 출력
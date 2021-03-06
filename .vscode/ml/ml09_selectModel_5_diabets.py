from sklearn.utils.testing import all_estimators
import numpy as np
import tensorflow as tf
from sklearn.datasets import load_iris,load_boston  ,load_diabetes #다중 분류모델
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,r2_score
from sklearn.svm import LinearSVC, SVC
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression  #회기가 아니라 분류이다
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

dataset = load_diabetes()

x = dataset.data
y= dataset.target
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,shuffle=True,random_state=66)

allAlgorithms = all_estimators(type_filter='regressor')

for (name, algorithms) in allAlgorithms:
    try:
        model = algorithms()

        model.fit(x_train,y_train)
        y_pred = model.predict(x_test)
        print(name,'의 정답률 : ', r2_score(y_test,y_pred))
    except:
        #continue
        print(name, '은 없는 놈!')
    
# ARDRegression 의 정답률 :  0.4987483503692143
# AdaBoostRegressor 의 정답률 :  0.36797624994694866
# BaggingRegressor 의 정답률 :  0.2710704123377842
# BayesianRidge 의 정답률 :  0.5008218932350129
# CCA 의 정답률 :  0.48696409064967594
# DecisionTreeRegressor 의 정답률 :  -0.20461499766279756
# DummyRegressor 의 정답률 :  -0.00015425885559339214
# ElasticNet 의 정답률 :  0.008101269711286885
# ElasticNetCV 의 정답률 :  0.43071557917754755
# ExtraTreeRegressor 의 정답률 :  -0.17596608751116816
# ExtraTreesRegressor 의 정답률 :  0.3986290286399231
# GammaRegressor 의 정답률 :  0.005812599388535289
# GaussianProcessRegressor 의 정답률 :  -5.636096407912189
# GeneralizedLinearRegressor 의 정답률 :  0.005855247171688949
# GradientBoostingRegressor 의 정답률 :  0.3884127026380264
# HistGradientBoostingRegressor 의 정답률 :  0.28899497703380905
# HuberRegressor 의 정답률 :  0.5033459728718326
# IsotonicRegression 은 없는 놈!
# KNeighborsRegressor 의 정답률 :  0.3968391279034368
# KernelRidge 의 정답률 :  -3.3847644323549924
# Lars 의 정답률 :  0.49198665214641635
# LarsCV 의 정답률 :  0.5010892359535759
# Lasso 의 정답률 :  0.3431557382027084
# LassoCV 의 정답률 :  0.49757816595208426
# LassoLars 의 정답률 :  0.36543887418957965
# LassoLarsCV 의 정답률 :  0.495194279067827
# LassoLarsIC 의 정답률 :  0.4994051517531072
# LinearRegression 의 정답률 :  0.5063891053505036
# LinearSVR 의 정답률 :  -0.33470258280275034
# MLPRegressor 의 정답률 :  -2.799710348720772
# MultiOutputRegressor 은 없는 놈!
# MultiTaskElasticNet 은 없는 놈!
# MultiTaskElasticNetCV 은 없는 놈!
# MultiTaskLasso 은 없는 놈!
# MultiTaskLassoCV 은 없는 놈!
# NuSVR 의 정답률 :  0.14471275169122277
# OrthogonalMatchingPursuit 의 정답률 :  0.3293449115305741
# OrthogonalMatchingPursuitCV 의 정답률 :  0.44354253337919747
# PLSCanonical 의 정답률 :  -0.975079227792292
# PLSRegression 의 정답률 :  0.4766139460349792
# PassiveAggressiveRegressor 의 정답률 :  0.4493811350774273
# PoissonRegressor 의 정답률 :  0.32989738735884344
# RANSACRegressor 의 정답률 :  0.1503945880051919
# RadiusNeighborsRegressor 의 정답률 :  -0.00015425885559339214
# RandomForestRegressor 의 정답률 :  0.35985508655430587
# RegressorChain 은 없는 놈!
# Ridge 의 정답률 :  0.40936668956159705
# RidgeCV 의 정답률 :  0.49525463889305044
# SGDRegressor 의 정답률 :  0.3933157471542975
# SVR 의 정답률 :  0.14331518075345895
# StackingRegressor 은 없는 놈!
# TheilSenRegressor 의 정답률 :  0.5176398294434736
# TransformedTargetRegressor 의 정답률 :  0.5063891053505036
# TweedieRegressor 의 정답률 :  0.005855247171688949
# VotingRegressor 은 없는 놈!
# _SigmoidCalibration 은 없는 놈!

# # TheilSenRegressor 의 정답률 :  0.5176398294434736 가장높음
#tensorflow keras모델과 비교해보자

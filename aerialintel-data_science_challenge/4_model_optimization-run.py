# MODEL OPTIMIZATION
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, RANSACRegressor
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle

# LOAD DATA
df = pd.read_csv('data/wheat-2013-supervised-edited.csv')
drop_cols = ['Latitude','Longitude'] + [df.columns[0]]
df.drop(drop_cols,axis=1,inplace=True)

# LOAD SBS FEATURES
with open('SBS_feat_set.plk','rb') as f:
    sbs_dict = pickle.load(f)

# PARAMETER TUNER
def tuner(name,*params):
    if name == 'Linear':
        k, model = 8, RANSACRegressor(base_estimator=LinearRegression(),max_trials=100,min_samples=params[0])
        X = np.matrix(df.ix[:,:-1])[:,list(sbs_dict[name][k])]
        y = np.array(df.ix[:,-1])
        X_std = StandardScaler().fit_transform(X)
        y_std = StandardScaler().fit_transform(y)
        X_train, X_test, y_train, y_test = train_test_split(X_std,y_std,test_size=0.25,random_state=42)    
    elif name == 'Random Forest':
        k, model = 4, RandomForestRegressor(n_estimators=params[0],max_depth=params[1],random_state=42)
        X = np.matrix(df.ix[:,:-1])[:,list(sbs_dict[name][k])]
        y = np.array(df.ix[:,-1])
        X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25,random_state=42) 
    elif name == 'Gradient Boost':
        k, model = 8, GradientBoostingRegressor(n_estimators=params[0],max_depth=params[1])
        X = np.matrix(df.ix[:,:-1])[:,list(sbs_dict[name][k])]
        y = np.array(df.ix[:,-1])
        X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.25,random_state=42) 
    results = model.fit(X_train,y_train)
    train_score = np.mean(cross_val_score(results,X_train,y_train,cv=8))
    test_score = results.score(X_test,y_test)
    return train_score, test_score

# EMPTY DICTS (will fill in w/ train & test scores)
train_dict = {}
test_dict = {}

################################################################
################# LINEAR REGRESSION w/ RANDSAC #################
################################################################
name = 'Linear'
test_scores = []
train_scores= []
param_list = []
min_samp_size = 70000
max_samp_size = 110000
for param in np.arange(min_samp_size,max_samp_size+1,10000):
    train_score, test_score = tuner(name,param)
    train_scores.append(train_score)
    test_scores.append(test_score)
    param_list.append(param)    
train_dict[name] = train_scores
test_dict[name] = test_scores


################################################################
################## RANDOM FOREST REGRESSOR #####################
################################################################
name = 'Random Forest'
test_scores = []
train_scores= []
param_list = []
min_trees,max_trees = 20,100
min_depth,max_depth = 1,5
for param1 in np.arange(min_trees,max_trees+1,20):
    bin1 = []
    bin2 = []
    param_list.append(param1)
    for param2 in np.arange(min_depth,max_depth+1,1):
        train_score, test_score = tuner(name,param1,param2)
        bin1.append(train_score)
        bin2.append(test_score)
    train_scores.append(np.array(bin1))
    test_scores.append(np.array(bin2))
train_dict[name] = train_scores
test_dict[name] = test_scores


################################################################
#################  GRADIENT BOOSTING REGRESSOR #################
################################################################
name = 'Gradient Boost'
test_scores = []
train_scores= []
param_list = []
min_trees,max_trees = 100,500
min_depth,max_depth = 1,5
for param1 in np.arange(min_trees,max_trees+1,100):
    bin1 = []
    bin2 = []
    param_list.append(param1)
    for param2 in np.arange(min_depth,max_depth+1,1):
        train_score, test_score = tuner(name,param1,param2)
        bin1.append(train_score)
        bin2.append(test_score)
    train_scores.append(np.array(bin1))
    test_scores.append(np.array(bin2))
train_dict[name] = train_scores
test_dict[name] = test_scores


# SAVE SCORES!
with open('model_optimization_train_scores.plk','wb') as f:
        pickle.dump(train_dict,f)
with open('model_optimization_test_scores.plk','wb') as f:
        pickle.dump(test_dict,f)
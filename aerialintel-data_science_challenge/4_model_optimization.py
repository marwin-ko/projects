# coding: utf-8
# # MODEL OPTIMIZATION

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, RANSACRegressor
from sklearn.cross_validation import train_test_split, cross_val_score
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle
#get_ipython().magic(u'matplotlib inline')
#import warnings
#warnings.filterwarnings('ignore')


# ## LOAD DATA
df = pd.read_csv('data/wheat-2013-supervised-edited.csv')
drop_cols = ['Latitude','Longitude'] + [df.columns[0]]
df.drop(drop_cols,axis=1,inplace=True)
#df.head()

# ## OPTIMIZE MODELS
with open('SBS_feat_set.plk','rb') as f:
    sbs_dict = pickle.load(f)

def optimizer(name,*params):
    if name == 'Linear':
        k, model = 8, RANSACRegressor(base_estimator=LinearRegression(),max_trials=100,min_samples=params[0])
    elif name == 'Random Forest':
        k, model = 4, RandomForestRegressor(n_estimators=params[0],max_depth=params[1],random_state=42)
    elif name == 'Gradient Boost':
        k, model = 8, GradientBoostingRegressor(n_estimators=params[0],max_depth=params[1])
        #k, model = 8, XGBRegressor(n_estimators=params[0],max_depth=params[1]) #XG Boost (same as gradient boost)
    X = np.matrix(df.ix[:,:-1])[:,list(sbs_dict[name][k])]#[:500]
    y = np.array(df.ix[:,-1])#[:500]
    X_std = StandardScaler().fit_transform(X)
    y_std = StandardScaler().fit_transform(y)
    X_train, X_test, y_train, y_test = train_test_split(X_std,y_std,test_size=0.25,random_state=42)
    results = model.fit(X_train,y_train)
    train_score = np.mean(cross_val_score(results,X_train,y_train,cv=8))
    test_score = results.score(X_test,y_test)
    return train_score, test_score


################
train_dict = {}
test_dict = {}
################


'''
name = 'Linear'
test_scores = []
train_scores= []
param_list = []
min_samp_size = 100#70000
max_samp_size = 200#100000
for param in np.arange(min_samp_size,max_samp_size+1,100): #10000):
    train_score, test_score = optimizer(name,param)
    train_scores.append(train_score)
    test_scores.append(test_score)
    param_list.append(param)    
plt.figure(figsize=(10,7))
plt.plot(param_list,train_scores,marker='^')
plt.plot(param_list,test_scores,marker='o')
plt.legend(['Train','Test'],loc=0)
plt.title('Linear Regression')
plt.xlabel('RANSAC Sample Size')
# plt.axis([min_samp_size,max_samp_size,0,1])
plt.ylabel('Score')
plt.grid(True)
#plt.show()
################################
train_dict[name] = train_scores
test_dict[name] = test_scores
plt.savefig('images/model_opt_{}.pdf'.format('LR'),format='pdf')
################################
'''

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
        train_score, test_score = optimizer(name,param1,param2)
        bin1.append(train_score)
        bin2.append(test_score)
    train_scores.append(np.array(bin1))
    test_scores.append(np.array(bin2))
################################
train_dict[name] = train_scores
test_dict[name] = test_scores
#plt.savefig('images/model_opt_{}.pdf'.format('RF'),format='pdf')
################################


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
        train_score, test_score = optimizer(name,param1,param2)
        bin1.append(train_score)
        bin2.append(test_score)
    train_scores.append(np.array(bin1))
    test_scores.append(np.array(bin2))
################################
train_dict[name] = train_scores
test_dict[name] = test_scores
#plt.savefig('images/model_opt_{}.pdf'.format('GB'),format='pdf')
################################


################################
with open('model_opt_train_scores.plk','wb') as f:
        pickle.dump(train_dict,f)
with open('model_opt_test_scores.plk','wb') as f:
        pickle.dump(test_dict,f)
################################



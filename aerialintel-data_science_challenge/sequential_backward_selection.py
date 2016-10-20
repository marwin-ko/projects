import numpy as np
from sklearn.base import clone
from itertools import combinations
from sklearn.cross_validation import train_test_split, cross_val_score

class SBS():
    def __init__(self, model, k_features,scoring_metric=cross_val_score, test_size=0.25, random_state=42):
        self.scoring_metric = scoring_metric
        self.model = clone(model)
        self.k_features = k_features
        self.test_size = test_size
        self.random_state = random_state
        
    def fit(self,X,y):
        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=self.test_size,random_state=self.random_state)
        dim = X_train.shape[1]
        self.indices_ = tuple(range(dim))
        self.subsets_ = [self.indices_]
        score = self._calc_score(X_train,y_train,X_test,y_test,self.indices_)
        self.scores_ = [score]
        
        while dim > self.k_features:
            scores = []
            subsets = []
            
            for p in combinations(self.indices_,r=dim-1):
                score = self._calc_score(X_train,y_train,X_test,y_test,p)
                scores.append(score)
                subsets.append(p)

            best = np.argmax(scores)
            self.indices_ = subsets[best]
            self.subsets_.append(self.indices_)
            dim -= 1
            self.scores_.append(scores[best])
        self.k_score_ = self.scores_[-1]
        return self
    
    def transform(self,X):
        return X[:,self.indices_]
    
    def _calc_score(self,X_train,y_train,X_test,y_test,indices):
        results = self.model.fit(X_train[:,indices],y_train)
        score = results.score(X_test[:,indices],y_test)
#         y_pred = self.model.predict(X_test[:,indices])
#         score = self.scoring_metric(y_test,y_pred)
#         score = np.mean(self.scoring_metric(self.model,X_train,y_train,scoring='r2'))
        return score 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.base import TransformerMixin
import pandas as pd
import csv
import re

class AsciiTransformer(TransformerMixin):
    def transform(self,X,**transform_params):     
        if str(type(X)) != "<class 'pandas.core.series.Series'>":
            X = pd.Series(X)
        return X.apply(lambda x: x.decode('ISO-8859-2').encode('ASCII','ignore'))
    def fit(self,X,y=None,**fit_params):
        return self

class LowerCaseTransformer(TransformerMixin):
    def transform(self,X,**transform_params):
        return pd.Series(X.apply(lambda x: x.lower()))
    def fit(self,X,y=None,**fit_params):
        return self
    
class RemoveSymsTransformer(TransformerMixin):
    def transform(self, X, **transform_params):
        return pd.Series(X.apply(lambda x: re.sub(re.compile(r'[^A-za-z0-9\s\.]'),' ',x)))
    def fit(self, X, y=None, **fit_params):
        return self

class RemoveStopWordsTransformer(TransformerMixin):
    def transform(self, X, **transform_params):
        with open('pt_stop_words.txt','rb') as f:
            stop = []
            reader = csv.reader(f)
            for word in reader:
                word = word[0].split()[0].decode('ISO-8859-2').encode('ASCII','ignore')
                if word == '':
                    pass
                else:
                    stop.append(word)
        return pd.Series(X.apply(lambda x: ' '.join([token for token in x.split() if token not in stop])))
    def fit(self, X, y=None, **fit_params):
        return self
    
class ZikaCounterTransformer(TransformerMixin):
    def transform(self,X,**transform_params):
        return pd.Series(X.apply(lambda x: len(re.findall(r'z.{2}a',x)))).values.reshape(-1,1)
    def fit(self,X,y=None,**fit_params):
        return self

class SentimentTransformer(TransformerMixin):
    def transform(self,X,**transform_params):
        matrix = []
        sa = SentimentIntensityAnalyzer()
        for text in X:
            senti = sa.polarity_scores(text)
            matrix.append([senti['pos'],senti['neu'],senti['neg'],senti['compound']])
        return pd.DataFrame(data=matrix,columns=['positive','neutral','negative','compound']).values
    def fit(self,X,y=None,**fit_params):
        return self 

## NOTES
# w2v/LDA using gensim for clustering
# POS tags
# Bi-Grams
# bigram_vectorizer = CountVectorizer(ngram_range=(1,2),min_df=1)
# bigrams = bigram_vectorizer.fit_transform(text).toarray()
# pd.DataFrame(bigrams, columns=bigram_vectorizer.get_feature_names())
# http://mccormickml.com/2016/04/12/googles-pretrained-word2vec-model-in-python/ 
# https://github.com/nltk/nltk/wiki/Sentiment-Analysis # spanish tweet corpus?
# http://www.slideshare.net/radiohead0401/running-word2vec-with-chinese-wikipedia-dump
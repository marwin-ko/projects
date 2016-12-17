from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.base import TransformerMixin
import pandas as pd
import csv
import re

class AsciiTransformer(TransformerMixin):
    def transform(self,X,**transform_params):     
        return pd.Series(X.apply(lambda x: x.decode('ISO-8859-2').encode('ASCII','ignore')))
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
'''
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
'''

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
        return pd.Series(X.apply(lambda x: len(re.findall(r'z.{2}a',x))))
    def fit(self,X,y=None,**fit_params):
        return self

class SentimentTransformer(TransformerMixin):
    def transform(self,X,**transform_params):
        def senti_pos(text):
            sa = SentimentIntensityAnalyzer()
            return sa.polarity_scores(text)['pos'] 
        def senti_neg(text):
            sa = SentimentIntensityAnalyzer()
            return sa.polarity_scores(text)['neg'] 
        def senti_neu(text):
            sa = SentimentIntensityAnalyzer()
            return sa.polarity_scores(text)['neu'] 
        def senti_com(text):
            sa = SentimentIntensityAnalyzer()
            return sa.polarity_scores(text)['compound'] 
        functs = [senti_pos, senti_neu, senti_neg, senti_com]
        matrix = []
        for text in X:
            senti = map(lambda x: x(text),functs)
            matrix.append(senti)
        return pd.DataFrame(data=matrix,columns=['positive','neutral','negative','compound'])
    def fit(self,X,y=None,**fit_params):
        return self  

## NOTES
# w2v/LDA using gensim for clustering
# POS tags
# Bi-Grams
# text = ['That is should come to this!', 'This above all: to thine own self be true.', 'Something is rotten in the state of Denmark.']
# bigram_vectorizer = CountVectorizer(ngram_range=(1,2),min_df=1)
# bigrams = bigram_vectorizer.fit_transform(text).toarray()
# pd.DataFrame(bigrams, columns=bigram_vectorizer.get_feature_names())
# http://mccormickml.com/2016/04/12/googles-pretrained-word2vec-model-in-python/ 
# https://github.com/nltk/nltk/wiki/Sentiment-Analysis # spanish tweet corpus?
# http://www.slideshare.net/radiohead0401/running-word2vec-with-chinese-wikipedia-dump
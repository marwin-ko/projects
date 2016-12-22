# GYANT: ZIKA CLASSIFICATION USING NLP


## MISSION STATEMENT
Utilizing anonymized raw text data, classify whether a person has Zika or not.


## APPROACH
1. __Exploratory Data Analysis (EDA)__
    * class imbalance ==> (zika ~ 500 samples | not_zika ~ 6500 samples)
    * determined encoding ==> ISO-8859-2 | ASCII | WINDOWS-1252
    * determined language ==> Portuguese (~98%+)

2. __Natural Language Processing (NLP) Pipeline__
    * Transform: decode ISO-8859-2 & encode ASCII
    * Transform: make all charaters lower case
    * Transform: remove symbols and special charaters
    * Transform: remove portuguese stop words
    * Feature Extraction (1 feats): count number of occurrences of the word "zika" (RegEx equivalent ==> [r'z.{2}a']) per document
    * Feature Extraction (4 feats): numerical sentiment polarity scores (positive, neutral, negative, compounded) were given per document 
    * Feature Extraction (n feats): performed latent semantic analysis (LSA), aka, I ran a TFIDF then a SVD(n components) on the processed text

3. __Training Model(s)__
    * Algorithms:
    * Parameters:
    * Metrics: 


## MODEL ANALYSIS



## SOLUTIONS
- more data
- word2vec
- latent dirichlet allocation (LDA)


## THANK YOU
I would like to thank the employers at GYANT for giving an opportunity to apply my NLP skillset in a machine learning application. If you wish to contact me, see below for my contact information:
* e-mail: marwinko19@gmail.com
* phone: (510)368-1756

# WALMART: PRODUCT CLASSIFICATION USING NLP


## MISSION STATEMENT
Classifying product tags using product information (text) to train a classification machine learning (ML) model(s).


## APPROACH
1. __Exploratory Data Analysis (EDA)__
    * review features (text)
    * review target frequency and distribution
    
2. __Natural Language Processing (NLP) Pipeline__
    * remove HTML tags
    * add space between camel case text
    * remove symbols
    * tokenize string (break text into tokens)
    * lemmatize tokens (similar to stemming, removes inflectional endings from words)
    * remove stop words (I used NLTK's stop words)
    * performed latent semantic analysis (LSA), aka, I ran a TFIDF then a SVD on the processed text.

3. __Training Model__
    * algorithm used: gradient boosting classifier (XG Boost)
    * why use XG Boost? I used XG Boost because it is a tree based model and learns from each tree sequentially. It out performed both Naive Bayes and Random Forest by at least 0.1 in accuracy score. I ultimately decided to stick with XG Boost and tune it's parameters (depth, learning rate, and number of trees) for an optimal model.
    * trained two models, both using XG Boost
    * trained one model on 'Product Long Description' and the other model on 'Product Name'

4. __Ensemble Model Predictions__
    * plugged test data, 'Product Long Description', into the model trained on 'Product Long Description'
    * plugged test data, 'product Name', into the model trained on 'Product Name'
    * if predictions from both models were the same, I just used that tag as the predicted output
    * if predictions from each model were different, then I combined the "different" predicted tags together.


## RUN MODEL
I used jupyter notebook. If you run the file named, "run_model.ipynb", then it should run. If you do not have jupyter notebook, you can visit my github project repo at https://github.com/marwin-ko/projects to see the code.


## THANK YOU
I would like to thank Walmart for hosting this Kaggle competition (Products on Virtual Shelves)! I was able to practice and use my NLP related skills for machine learning applications. My RegEx game went up a couple notches after this competition/project, haha. If you wish to contact me, see below for my contact information:
* e-mail: marwinko19@gmail.com
* phone: (510)368-1756
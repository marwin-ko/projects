# AERIAL INTELLIGENCE: WINTER WHEAT YIELD PREDICTION


## MISSION STATEMENT
Predicting wheat yield in the Winter (data provided by Aerial Intelligence) by using trained regression machine learning (ML) model(s).


## APPROACH
I approached this project by doing the following items in sequential order:

1. Preprocessing Data
    * remove samples (rows) with missing data
    * remove useless features (columns) with zero variance
2. Exploratory Data Analysis (EDA)
    * review feature(s) distributions
    * review target distribution (to help determine a proper train/test/split)
3. Feature Selection
    * run/evaluate ML algorithms
    * evaluate feature importances
    * run sequential backward selection (SBS) for further feature selection insight
4. Model Optimization
    * trained ML model on 2013 wheat data
    * MODELS USED: Linear Regression, Random Forrest Regressor, Gradient Boosting Regressor
    * Linear Regression: I utilized RANSAC (random sampling consensus) method and tuned the same size number
    * Random Forest and Gradient Boost: I tuned number of trees and depth
    * save and pickle model for future use
5. Model Analysis
    * tested ML model on 2014 wheat data
    * evaluated residuals over predicted values
    * evaluated predicted values over true values


## TRAIN/TEST MODEL 
* I utilized the 2013 wheat yield data to train my ML model; 75% and 25% for train and test, respectively.
* I utilized the 2014 wheat yield data to test my trained models.


## MODEL ANALYSIS
I trained 3 different models: Linear Regression (LR), Random Forest Regressor (RF), and Gradient Boosting Regressor (GB). My idea behind training so many different models was to be able to ensemble model them later on (i.e. take all predictions and average them to obtain one final (hopefully accurate as well) prediction. Unfortunately, not all models performed well and so no model ensemble was performed.

### LINEAR REGRESSION
The LR model did not perform well. When I tested the model on the 2014 data, 95%+ of the data was underestimated and 50%+ of the data was negative predictions. How do you get negative yield? The answer is, you can't. This is my third project using LR and I am starting to realize that LR is not very robust ML algorithm.

### RANDOM FOREST REGRESSOR
The RF model perforance was fair. Although my final RF model underestimates and overestimates a fair amount I believe that if I spend even more time selecting features carefully, then the RF would have performed better.

### GRADIENT BOOSTING REGRESSOR
The GB model performance is similar to RF, but tends to underestimate and overestimate more extreme.


## CHALLENGES FACED
Feature selection was definitely the biggest challenge I faced and where a bulk of my time was spent. Upon the first evaluation of feature importances, almost 100% of the feature weights were on the longitude and latitude features only. After further evaluation, I determined that the relationship between longitude and latitude relative to the wheat yield was a form of _data leakage_. As a result, I removed the longitude and latitude features. Another challenge was to determine whether or not to remove features suggested by the SBS algorithm. 


## FUTURE PLANS
If I had more time to spend on this project, I would improve the model accuracy and implement in a flask app with d3 visualization.

### MODEL IMPROVEMENT I
How would I improve the model? Well, first I would create several different models using Random Forest (since it was the "best" performing ML algorithm that I ran) in conjunction with different feature selections. After I create these several models, I would evaluate each model to see whether they are under or over predicting then select k models that would compliment each other in an ensemble voting method (taking predictions from multiple models and then averaging them for a final prediction).

### MODEL IMPROVEMENT II
Another idea I had to potential improve the models, is to bin the wheat yields and treat this problem as a classification problem. Might not be the best or conventional idea, but it would be worth a shot.

### MODEL IMPROVEMENT III
Train all of 2013 and most of 2014, then test on a small holdout set from 2014. I actually did this earlier and obtained better predictions, however, I opted to move forward with just training on 2013. Not training on more data was a huge mistake and I will know better for future projects.

### FLASK APP & D3 VISUAL
If I had more time available, I would create a flask app. In my imaginary app, the user (wheat farmers) could input several features into text boxes and the app would output the wheat yield prediction. The cherry on top would be a d3 visual showing the wheat yield in the form of a grid populated with green boxes in it; displaying the wheat yield in the form of those green boxes. If end up making the app, I will post the link or code to it on this github repo.


## THANK YOU
I would like to thank Aerial Intelligence for giving me this opportunity to practice, learn, and showcase my skills as a data scientist. If you wish to contact me, see below for such information:
* e-mail: marwinko19@gmail.com
* phone: (510)368-1756
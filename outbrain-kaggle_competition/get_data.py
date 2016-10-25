import os

URLS = ['https://www.kaggle.com/c/outbrain-click-prediction/download/documents_categories.csv.zip',
        'https://www.kaggle.com/c/outbrain-click-prediction/download/clicks_test.csv.zip',
        'https://www.kaggle.com/c/outbrain-click-prediction/download/documents_meta.csv.zip',
        'https://www.kaggle.com/c/outbrain-click-prediction/download/documents_entities.csv.zip',
        'https://www.kaggle.com/c/outbrain-click-prediction/download/promoted_content.csv.zip',
        'https://www.kaggle.com/c/outbrain-click-prediction/download/sample_submission.csv.zip',
        'https://www.kaggle.com/c/outbrain-click-prediction/download/documents_topics.csv.zip',
        'https://www.kaggle.com/c/outbrain-click-prediction/download/clicks_train.csv.zip',
        'https://www.kaggle.com/c/outbrain-click-prediction/download/events.csv.zip',
        'https://www.kaggle.com/c/outbrain-click-prediction/download/page_views.csv.zip',
        'https://www.kaggle.com/c/outbrain-click-prediction/download/page_views_sample.csv.zip']

for URL in URLS:
    os.system('wget {} -P data'.format(URL))
    print '######## FINISHED! ==> {} ########'.format(URL[59:])
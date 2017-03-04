from elasticsearch import Elasticsearch
from random import randint
import os, requests

def check_ES():
	try:
		res = requests.get('http://localhost:9200')
		print('Elasticsearch is up and running!')
	except:
		print('Elasticsearch not running!')
		print('Starting Elasticsearch...')
		os.system('/Users/marwinko/Public/elasticsearch-5.2.2/bin/elasticsearch')
		print('Elasticsearch is up and running!')

def input_users():
	es = Elasticsearch([{'host': 'localhost', 'port': 9200}],http_auth=('elastic','changeme'))
	for i in range(1,2000001):
		doc = {'email':'name_'+str(i)+'@email.com',
			'number': randint(1,10000),
			'company': 'company_'+str(randint(1,10000)),
			'school': 'school_'+str(randint(1,1000))}
		es.index(index="users", doc_type='people', id=i, body=doc)
	print('Users entered!')

check_ES()
input_users()

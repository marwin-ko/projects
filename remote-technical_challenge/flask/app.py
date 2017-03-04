from flask import Flask
from elasticsearch import Elasticsearch
app = Flask(__name__)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}], http_auth=('elastic', 'changeme'))
#######################################################
# GET specific user info
@app.route('/remote/api/v1.0/users', methods = ['GET'])
def get_user_info():
    user_id = input('Enter user id: ')
    return jsonify(es.search(index='users',body={'query': {'match': {'_id':user_id}}})['hits']['hits'][0]['_source'])
#######################################################
# GET specific user 1st degree connection
@app.route('/remote/api/v1.0/users', methods = ['GET'])
def user_1st_degree():
    user_id = input('Enter user id: ')
    user_info = es.search(index='users',body={'query': {'match': {'_id':user_id}}})['hits']['hits'][0]['_source']
    coworkers = es.search(index='users',body={'query': {'match': {'company':user_info['company']}}})['hits']['hits']
    coworker_ids = [coworker['_id'] for coworker in coworkers]
    classmates = es.search(index='users',body={'query': {'match': {'school':user_info['school']}}})['hits']['hits']
    classmate_ids = [classmate['_id'] for classmate in classmates]
    first_conns = list(set(coworker_ids+classmate_ids))
    return jsonify({'1st_deg_conns': first_conns})
#######################################################
# GET specific user 2nd degree connection
def user_1st_degreex(user_id):
    # this user_1st_degreex function has an input arg
    # which is utilized in the user_2nd_degree function
    user_info = es.search(index='users',body={'query': {'match': {'_id':user_id}}})['hits']['hits'][0]['_source']
    coworkers = es.search(index='users',body={'query': {'match': {'company':user_info['company']}}})['hits']['hits']
    coworker_ids = [coworker['_id'] for coworker in coworkers]
    classmates = es.search(index='users',body={'query': {'match': {'school':user_info['school']}}})['hits']['hits']
    classmate_ids = [classmate['_id'] for classmate in classmates]
    first_conns = list(set(coworker_ids+classmate_ids))
    return first_conns
@app.route('/remote/api/v1.0/users', methods = [''])
def user_2nd_degree():
    # From your 1st degree connections, get their 1st degree connections...this will yield your 2nd degree connections
    user_id = input('Enter user id: ')
    first_conns = user_1st_degreex(user_id)
    second_conns = []
    for conn in first_conns:
        second_conns.extend(user_1st_degree(conn))
    unique_second_conns = list(set(second_conns))
    return unique_second_conns
#######################################################
# PUT update user
@app.route('/remote/api/v1.0/users', methods = ['PUT'])
def update_user():
    print('You are about to update a user\'s information.')
    print(' ')
    answer = input('Do you wish to continue? Y/N ')
    if answer.upper() == 'Y':
        user_id = input('Enter user id: ')
        print('Please update the following information.')
        email = input('email: ')
        number = input('number: ')
        company = input('company: ')
        school = input('school: ')
        doc = {'email': email,
           'number': int(number),
           'company': company,
           'school': school}
        es.index(index, doc_type, body, id=user_id)
        return jsonify({'Update': True})
    else:
        return jsonify({'Update': False})
#######################################################
# POST (create new user)
@app.route('/remote/api/v1.0/users', methods = ['POST'])
def add_user():
    # Can also implement request.json
    print('Please fill out the following information.')
    email = input('email: ')
    number = input('number: ')
    company = input('company: ')
    school = input('school: ')
    doc = {'email': email,
           'number': int(number),
           'company': company,
           'school': school}
    # add in new user...welcome to Remote.com! :)
    es.index(index='users',doc_type='people',id=es.count(index='users')['count']+1,body=doc)
    return jsonify({'doc':doc}),201
#######################################################
# DELETE (delete user)
@app.route('/remote/api/v1.0/users',methods=['DELETE'])
def delete_user():
    # Delete user based off ID in the users index
    print('###########################################')
    print('################# WARNING #################')
    print('###########################################')
    print('You are about to delete a user from Remote.')
    print(' ')
    answer = input('Do you wish to continue? Y/N ')
    if answer.upper() == 'Y':
        user_id = input('Enter user ID: ')
        es.delete(index='users',doc_type='people',id=int(user_id))
        print('You have removed User_%s from Remote.com. :(' % user_id)
        return jsonify({'result':True})
    else:
        return jsonify({'result':False})
#######################################################
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}),404)
#######################################################
if __name__ == '__main__':
    app.run(debug=True)
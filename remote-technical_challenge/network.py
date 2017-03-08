def create_company_network():
    company_network = {}
    for i in range(1,10001):
        employees = es.search(index='users',body={'query':{'match':{'company':'company_'+str(i)}}})['hits']['hits']
        user_ids = [user['_id'] for user in employees]
        company_network['company_'+str(i)] = user_ids
    return company_network

def create_school_network():
    school_network = {}
    for i in range(1,1001):
        classmates = es.search(index='users',body={'query':{'match':{'school':'school_'+str(i)}}})['hits']['hits']
        user_ids = [user['_id'] for user in classmates]
        school_network['school_'+str(i)] = user_ids    
    return school_network
    
def create_user_network():
    company_network = create_company_network()
    school_network = create_school_network()
    user_network = {}
    # first degree
    for i in range(1,1001):
        company = es.search(index='users',body={'query':{'match':{'_id':str(1)}}})['hits']['hits'][0]['_source']['company']
        school = es.search(index='users',body={'query':{'match':{'_id':str(1)}}})['hits']['hits'][0]['_source']['school']
        first_degree  = list(set(company_network[company] + school_network[school]))
        user_network['id_'+str(i)]['first_degree'] = first_degree
    #second degree
    for i in range(1,1001):
        first_degree = user_network['id_'+str(i)]['first_degree']
        second_degree = []
        for user in first_degree:
            extended_connections = user_network['id_'+user]['first_degree']
            second_degree.append(extended_connections)
        user_network['id_'+str(i)]['second_degree'] = list(set(second_degree))
    return user_network
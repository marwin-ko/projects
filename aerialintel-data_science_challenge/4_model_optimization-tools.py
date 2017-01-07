# MODEL OPTIMIZATION

def model_trainer(model,X,y):
    X_std = StandardScaler().fit_transform(X)
    y_std = StandardScaler().fit_transform(y)
    X_train, X_test, y_train, y_test = train_test_split(X_std,y_std,test_size=0.25,random_state=42)
    trained_model = model.fit(X_train,y_train)
    return trained_model

def model_scores(model_name,X,y,*params):
    if model_name == 'Linear':
        model = RANSACRegressor(base_estimator=LinearRegression(),max_trials=100,min_samples=params[0])
    elif model_name == 'Random Forest':
        model = RandomForestRegressor(n_estimators=params[0],max_depth=params[1],random_state=42)
    elif name == 'Gradient Boost':
        model = GradientBoostingRegressor(n_estimators=params[0],max_depth=params[1])
    X_std = StandardScaler().fit_transform(X)
    y_std = StandardScaler().fit_transform(y)
    X_train, X_test, y_train, y_test = train_test_split(X_std,y_std,test_size=0.25,random_state=42)
    results = model.fit(X_train,y_train)
    train_score = np.mean(cross_val_score(results,X_train,y_train,cv=8))
    test_score = results.score(X_test,y_test)
    return train_score, test_score

def linear_model_tuner(model,X,y,
                       min_samp,max_samp,step_samp):
    #using RANDSAC approach
    train_scores, test_scores, param_list = [],[],[]
    for sample_size in np.arange(min_samp_size,max_samp_size+1,step_samp):
        train_score, test_score = model_scores(model,X,y,sample_size)        
        train_scores.append(train_score)
        test_scores.append(test_score)
        param_list.append(param)
    return param_list, train_scores, test_scores

def tree_model_tuner(model,X,y,
                     min_trees,max_trees,step_trees,
                     min_depth,max_depth,step_depth)
    train_scores, test_scores, param_list = [],[],[]
    for n_trees in np.arange(min_trees,max_trees+1,step_trees):
        bin1,bin2 = [],[]
        param_list.append(n_trees)
        for n_depth in np.arange(min_depth,max_depth+1,step_trees):
            train_score, test_score = model_scores(model,X,y,n_tree,n_depth)
            bin1.append(train_score)
            bin2.append(test_score)
        train_scores.append(np.array(bin1))
        test_scores.append(np.array(bin2))
    return param_list, train_scores, test_scores

def tree_grapher(name,param_list,train_scores,test_scores):
    fig,axs = plt.subplots(nrows=1,ncols=2)
    fig.set_figheight(7)
    fig.set_figwidth(15)
    ax = axs[0]
    ax.plot(param_list,train_scores,marker='^')
#    ax.legend(['n_depth={}'.format(n) for n in np.arange(1,max_depth+1,1)],loc=3)
    ax.set_title('MODEL:{} (Train)'.format(name))
    ax.set_xlabel('n Trees')
    ax.set_ylabel('Score')
    ax.grid(True)
    ax = axs[1]
    ax.plot(param_list,test_scores,marker='o')
#    ax.legend(['n_depth={}'.format(n) for n in np.arange(1,max_depth+1,1)],loc=3)
    ax.set_title('MODEL:{} (Test)'.format(name))
    ax.set_xlabel('n Trees')
    ax.set_ylabel('Score')
    ax.grid(True)

def linear_grapher(name,param_list,train_scores,test_scores):
    plt.figure(figsize=(10,7))
    plt.plot(param_list,train_scores,marker='^')
    plt.plot(param_list,test_scores,marker='o')
    plt.legend(['Train','Test'],loc=0)
    plt.title('MODEL:{}'.format(name))
    plt.xlabel('RANSAC Sample Size')
    plt.ylabel('Score')
    plt.grid(True)
    plt.show()
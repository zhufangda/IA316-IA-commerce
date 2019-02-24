import requests

envs_url = {'first':'http://52.47.62.31/', 
            'second':'http://35.180.254.42/',
            'third' : 'http://35.180.178.243/'
           }
user_id = '9Z1XVDNFAG2Y3ZYEKOIL'

def req_reset(envs='first', verbose=False):
    '''
        Send reset request to the API for different environment.

        Params:
            envs: the name of the environement, it could be 'first', 'second' and 'third'
            verbose: show description of response if true       

        Returns:
            dict: response of api.
                 if 'envs' == 'first':
                     ------Summary-----
                    key:	item_history,   type:	<class 'int'>
                    key:	nb_items,   type:<class 'int'>
                    key:	nb_users, 	type:<class 'int'>
                    key:	next_item,  type:<class 'int'>	
                    key:	next_user, 		value:	41
                    key:	rating_history, 		size:	10000, 		type:	<class 'int'>
                    key:	user_history, 		size:	10000, 		type:	<class 'int'> 
                if 'envs' == 'second'
                key:	item_history, 		size:	2000, 		type:	<class 'int'>
                    key:	nb_items, 		value:	300
                    key:	nb_users, 		value:	100
                    key:	next_item, 		value:	292
                    key:	next_user, 		value:	60
                    key:	next_variables, 		size:	5, 		type:	<class 'float'>
                    key:	rating_history, 		size:	2000, 		type:	<class 'int'>
                    key:	user_history, 		size:	2000, 		type:	<class 'int'>
                    key:	variables_history, 		size:	2000, 		type:	<class 'list'>
                if 'envs' == 'third':
                    key:	action_history, 		size:	200, 		type:	<class 'int'>
                    key:	nb_items, 		value:	30
                    key:	nb_users, 		value:	100
                    key:	next_state, 		size:	30, 		type:	<class 'list'>
                    key:	rewards_history, 		size:	200, 		type:	<class 'int'>
                    key:	state_history, 		size:	200, 		type:	<class 'list'>
                    key:	item_history, 		size:	2000, 		type:	<class 'int'>


    '''

    params = {
            "user_id":user_id
        }
    
    response = requests.get(envs_url[envs] + 'reset', params=params)
    data = response.json()
    
    if verbose:
        print('------Summary-----')
        for key in data.keys():
            ele = data[key]
            if type(ele) is list:
                print(f'key:{key}, \tsize:{len(ele)}, \ttype:{type(ele[0])}')
            else:
                print(f'key:\t{key}, \tvalue:\t{ele}')
    return data


def req_predict(predict, envs='first', verbose=False):
    '''
        Send predict  request to the API for different environment.

        Params:
            predict: the predict rating for first and second enviroment, reccomendation_item for third environement
            envs: the name of the environement, it could be 'first', 'second' and 'third'
            verbose: show verbose if true 

        Returns:
            data : the API response;
                if envs == first
                    key:	next_item
                    key:	next_user
                    key:	rating
                if envs == third:
                    key:	next_item
                    key:	next_user
                    key:	rating      



    '''
    params = {
        "user_id":user_id,
        "predicted_score":predict
    }
    
    
    if envs=='third':
        params['recommended_item'] = predict

    response = requests.get(url= envs_url[envs]+'predict', params=params)
    data = response.json()
    
    if verbose:
        print('------Summary-----')
        for key in data.keys():
            ele = data[key]
            if type(ele) is list:
                print(f'key:{key},\tsize:{len(ele)},\ttype:{type(ele[0])}')
            else:
                print(f'key:{key},\tvalue:{ele}')
                
    return data

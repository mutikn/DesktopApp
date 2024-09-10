import requests

DOMAIN_NAME = 'https://f7fe-82-194-23-237.ngrok-free.app/'

def register(email, password, password2):
    post_url = f'{DOMAIN_NAME}register/'

    response = requests.post(post_url, json={
        "email": email,
        "password": password,
        "password2": password2
    })

    if response.status_code == 201:
        answer = response.json().get('STATUS')
        return True, str(answer) 

    return False, str(response.text)  


def get_token(email, password):
    post_url = f'{DOMAIN_NAME}api-token-auth/'

    response = requests.post(post_url, json={
        "username": email,
        "password": password
    })

    if response.status_code == 200:
        return True, str(response.json().get('token')) 
    
    return False, str(response.text)  


def get_active_users(token):    
    get_url = f'{DOMAIN_NAME}get_active_users/'
    list_of_active_users = []

    response = requests.get(get_url, headers={
        'Authorization': f'Token {token}'
    })

    for users in response.json():
        list_of_active_users.append(users.get('email'))

    return list_of_active_users


def get_comments(token):
    get_url= f'{DOMAIN_NAME}comments/'

    response = requests.get(get_url, headers={
        'Authorization': f'Token {token}'
    })
    
    return response.json()


def add_comment(token, comment):
    post_url = f'{DOMAIN_NAME}comments/'

    response = requests.post(post_url, 
        headers={'Authorization': f'Token {token}'}, json={'comment': comment})

    return response.json()

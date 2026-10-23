import requests

def register_user(email, password):
    url = 'https://graph.microsoft.com/v1.0/users'
    headers = {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
        'Content-Type': 'application/json'
    }
    data = {
        'accountEnabled': True,
        'displayName': email.split('@')[0],
        'mailNickname': email.split('@')[0],
        'userPrincipalName': email,
        'passwordProfile': {
            'forceChangePasswordNextSignIn': True,
            'password': password
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return 'User registered successfully'
    else:
        return 'Failed to register user'
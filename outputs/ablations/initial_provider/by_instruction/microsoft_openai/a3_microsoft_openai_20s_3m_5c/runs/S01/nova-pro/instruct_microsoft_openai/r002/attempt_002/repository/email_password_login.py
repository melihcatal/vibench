import requests

def email_password_login(email, password):
    url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    data = {
        'grant_type': 'password',
        'client_id': 'YOUR_CLIENT_ID',
        'scope': 'openid profile email',
        'username': email,
        'password': password,
        'client_secret': 'YOUR_CLIENT_SECRET'
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        return 'Failed to login'
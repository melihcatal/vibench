import requests

def refresh_session(refresh_token):
    url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    data = {
        'grant_type': 'refresh_token',
        'client_id': 'YOUR_CLIENT_ID',
        'scope': 'openid profile email',
        'refresh_token': refresh_token,
        'client_secret': 'YOUR_CLIENT_SECRET'
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        return 'Failed to refresh session'
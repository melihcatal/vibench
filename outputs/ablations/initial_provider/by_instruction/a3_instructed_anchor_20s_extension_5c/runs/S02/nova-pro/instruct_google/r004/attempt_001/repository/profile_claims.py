import requests

def profile_claims(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None
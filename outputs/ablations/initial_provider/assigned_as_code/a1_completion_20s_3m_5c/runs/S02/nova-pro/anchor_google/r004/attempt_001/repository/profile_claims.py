import requests

def fetch_user_profile(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://oauth.provider.com/userinfo', headers=headers)
    response.raise_for_status()
    user_profile = response.json()
    return {
        'sub': user_profile.get('sub'),
        'name': user_profile.get('name'),
        'email': user_profile.get('email')
    }
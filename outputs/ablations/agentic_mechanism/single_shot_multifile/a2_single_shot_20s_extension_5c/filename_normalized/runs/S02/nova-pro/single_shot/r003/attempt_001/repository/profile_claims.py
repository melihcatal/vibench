import requests

def profile_claims(access_token):
    PROFILE_ENDPOINT = 'https://www.googleapis.com/oauth2/v3/userinfo'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(PROFILE_ENDPOINT, headers=headers)
    response.raise_for_status()
    claims = response.json()
    return {
        'sub': claims.get('sub'),
        'name': claims.get('name'),
        'email': claims.get('email')
    }
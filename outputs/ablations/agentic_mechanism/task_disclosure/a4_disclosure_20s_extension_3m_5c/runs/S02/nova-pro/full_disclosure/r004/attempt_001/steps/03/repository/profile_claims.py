import requests

# Google OAuth2 provider configuration
GOOGLE_OAUTH2_USERINFO_ENDPOINT = 'https://oauth2.googleapis.com/tokeninfo'

def fetch_and_normalize_profile_claims(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(GOOGLE_OAUTH2_USERINFO_ENDPOINT, headers=headers)
    response.raise_for_status()
    user_info = response.json()
    
    # Normalize profile claims
    normalized_claims = {
        'sub': user_info.get('sub'),
        'name': user_info.get('name'),
        'given_name': user_info.get('given_name'),
        'family_name': user_info.get('family_name'),
        'email': user_info.get('email'),
        'picture': user_info.get('picture')
    }
    return normalized_claims
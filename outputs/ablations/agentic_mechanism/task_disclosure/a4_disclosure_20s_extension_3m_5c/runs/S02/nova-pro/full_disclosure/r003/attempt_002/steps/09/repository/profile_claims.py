import requests


def fetch_profile_claims(access_token):
    """Fetches and normalizes federated user profile claims from Google."""
    url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    profile_data = response.json()
    normalized_claims = {
        'user_id': profile_data.get('id'), 
        'name': profile_data.get('name'), 
        'email': profile_data.get('email'), 
        'picture': profile_data.get('picture')
    }
    return normalized_claims

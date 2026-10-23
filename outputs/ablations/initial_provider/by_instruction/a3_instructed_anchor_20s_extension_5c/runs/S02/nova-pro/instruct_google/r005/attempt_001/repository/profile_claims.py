import requests

def fetch_profile_claims(access_token):
    url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        profile = response.json()
        normalized_profile = {
            'id': profile.get('id'),
            'name': profile.get('name'),
            'email': profile.get('email'),
            'picture': profile.get('picture')
        }
        return normalized_profile
    else:
        raise Exception('Failed to fetch profile claims')

if __name__ == '__main__':
    access_token = input('Enter the access token: ')
    profile_claims = fetch_profile_claims(access_token)
    print(profile_claims)
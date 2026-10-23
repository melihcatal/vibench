import requests

GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0/me'

def fetch_profile_claims(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(GRAPH_API_ENDPOINT, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    pass
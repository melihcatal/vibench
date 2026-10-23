import requests

COGNITO_DOMAIN = "your-cognito-domain"
COGNITO_CLIENT_ID = "your-cognito-client-id"

def fetch_profile_claims(access_token):
    url = f"https://{COGNITO_DOMAIN}/oauth2/userInfo"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
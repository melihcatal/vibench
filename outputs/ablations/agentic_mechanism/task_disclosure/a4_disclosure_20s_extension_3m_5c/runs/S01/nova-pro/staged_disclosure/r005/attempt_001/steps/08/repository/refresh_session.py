import os
import requests

# Google OAuth2 configuration
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('GOOGLE_REFRESH_TOKEN')

def refresh_google_token():
    url = 'https://oauth2.googleapis.com/token'
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN,
        'grant_type': 'refresh_token'
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    new_tokens = refresh_google_token()
    print(new_tokens)
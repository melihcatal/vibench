import requests

CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'
CLIENT_SECRET = 'YOUR_GOOGLE_CLIENT_SECRET'
REDIRECT_URI = 'YOUR_REDIRECT_URI'
TOKEN_URI = 'https://oauth2.googleapis.com/token'

def exchange_code_for_tokens(code: str) -> dict:
    token_data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    response = requests.post(TOKEN_URI, data=token_data)
    response.raise_for_status()
    return response.json()

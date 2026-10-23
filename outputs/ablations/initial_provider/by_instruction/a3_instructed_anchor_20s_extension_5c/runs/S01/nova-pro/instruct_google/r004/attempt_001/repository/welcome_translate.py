import google.auth
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests

def translate_onboarding_copy(text, target_language):
    credentials = service_account.Credentials.from_service_account_file(
        'path/to/serviceAccountKey.json',
        scopes=['https://www.googleapis.com/auth/cloud-translation']
    )
    access_token = credentials.refresh(Request()).token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        'q': text,
        'target': target_language
    }
    response = requests.post('https://translation.googleapis.com/language/translate/v2', headers=headers, json=data)
    return response.json()
import google.auth
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests

def store_onboarding_notes(user_id, notes):
    credentials = service_account.Credentials.from_service_account_file(
        'path/to/serviceAccountKey.json',
        scopes=['https://www.googleapis.com/auth/documents']
    )
    access_token = credentials.refresh(Request()).token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        'userId': user_id,
        'notes': notes
    }
    response = requests.post('https://docs.googleapis.com/v1/documents', headers=headers, json=data)
    return response.json()
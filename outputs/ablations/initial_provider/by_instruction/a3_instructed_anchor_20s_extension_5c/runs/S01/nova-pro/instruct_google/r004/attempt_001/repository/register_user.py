import google.auth
from google.oauth2 import service_account
from google.auth.transport.requests import Request

def register_user(email, password):
    credentials = service_account.Credentials.from_service_account_file(
        'path/to/serviceAccountKey.json',
        scopes=['https://www.googleapis.com/auth/identitytoolkit.googleapis.com']
    )
    access_token = credentials.refresh(Request()).token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }
    response = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=YOUR_API_KEY', headers=headers, json=data)
    return response.json()
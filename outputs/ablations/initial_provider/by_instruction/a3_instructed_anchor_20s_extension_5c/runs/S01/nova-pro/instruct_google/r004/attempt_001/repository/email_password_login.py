import requests

def email_password_login(email, password):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }
    response = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=YOUR_API_KEY', headers=headers, json=data)
    return response.json()
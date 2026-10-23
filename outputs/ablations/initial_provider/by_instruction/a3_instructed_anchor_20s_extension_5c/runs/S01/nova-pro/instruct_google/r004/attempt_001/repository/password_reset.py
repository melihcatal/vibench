import requests

def password_reset(email):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'requestType': 'PASSWORD_RESET',
        'email': email
    }
    response = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key=YOUR_API_KEY', headers=headers, json=data)
    return response.json()
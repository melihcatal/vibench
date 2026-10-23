import requests

def refresh_session(refresh_token):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post('https://securetoken.googleapis.com/v1/token?key=YOUR_API_KEY', headers=headers, json=data)
    return response.json()
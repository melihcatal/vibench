import os
import requests
from flask import Flask, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.urandom(24)

GOOGLE_CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'
GOOGLE_CLIENT_SECRET = 'YOUR_GOOGLE_CLIENT_SECRET'
GOOGLE_DISCOVERY_URL = (
    'https://accounts.google.com/.well-known/openid-configuration'
)

@app.route('/')
def index():
    if 'profile' not in session:
        return redirect(url_for('login'))
    return f'Hello, {session['profile']['name']}!'

@app.route('/login')
def login():
    authorization_url = google_oauth_authorization_url()
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    code = request.args.get('code')
    tokens = get_tokens(code)
    session['tokens'] = tokens
    profile = get_profile()
    session['profile'] = profile
    return redirect(url_for('index'))

def google_oauth_authorization_url():
    response = requests.get(GOOGLE_DISCOVERY_URL)
    authorization_endpoint = response.json()['authorization_endpoint']
    return (
        f'{authorization_endpoint}?response_type=code'
        f'&client_id={GOOGLE_CLIENT_ID}'
        f'&redirect_uri=http://localhost:5000/oauth2callback'
        f'&scope=openid+email+profile'
        f'&access_type=offline'
    )

def get_tokens(code):
    token_url = response.json()['token_endpoint']
    payload = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': 'http://localhost:5000/oauth2callback',
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=payload)
    return response.json()

def get_profile():
    userinfo_url = response.json()['userinfo_endpoint']
    token = session['tokens']['access_token']
    response = requests.get(userinfo_url, headers={'Authorization': f'Bearer {token}'})
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
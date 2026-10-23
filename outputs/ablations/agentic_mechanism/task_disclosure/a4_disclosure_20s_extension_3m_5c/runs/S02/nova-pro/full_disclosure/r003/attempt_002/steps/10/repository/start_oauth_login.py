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
    return f'Hello, {session['profile']['name']}.\n<a href=\"/logout\">Logout</a>'

@app.route('/login')
def login():
    random_state = os.urandom(24)
    session['state'] = random_state
    authorization_url = (
        'https://accounts.google.com/o/oauth2/v2/auth'
    )
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': 'http://localhost:5000/callback',
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': random_state,
    }
    return redirect(authorization_url + '?' + urlencode(params))

@app.route('/callback')
def callback():
    code = request.args.get('code')
    state = request.args.get('state')
    if state!= session['state']:
        return 'State does not match. Please try again.'
    token_url = 'https://oauth2.googleapis.com/token'
    token_payload = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': 'http://localhost:5000/callback',
        'grant_type': 'authorization_code',
    }
    token_response = requests.post(token_url, data=token_payload)
    token_response.raise_for_status()
    token_data = token_response.json()
    userinfo_url = 'https://openidconnect.googleapis.com/v1/userinfo'
    userinfo_headers = {'Authorization': 'Bearer ' + token_data['access_token']}
    userinfo_response = requests.get(userinfo_url, headers=userinfo_headers)
    userinfo_response.raise_for_status()
    session['profile'] = userinfo_response.json()
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('profile', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
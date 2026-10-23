import os
from flask import Flask, request
from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)

@app.route('/oauth_callback', methods=['GET'])
def oauth_callback():
    auth_code = request.args.get('code')
    try:
        id_info = id_token.verify_oauth2_token(auth_code, requests.Request(), os.getenv('GOOGLE_CLIENT_ID'))
        if id_info['aud']!= os.getenv('GOOGLE_CLIENT_ID'):
            raise ValueError('Invalid audience.')
        user_id = id_info['sub']
        access_token = id_info['access_token']
        return {'user_id': user_id, 'access_token': access_token}
    except ValueError:
        return 'Invalid token', 400

if __name__ == '__main__':
    app.run(port=5000)
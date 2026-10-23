import os
import flask
from google.oauth2 import id_token
from google.auth.transport import requests

app = flask.Flask(__name__)

@app.route('/oauth_callback')
def oauth_callback():
    code = flask.request.args.get('code')
    try:
        token = id_token.verify_oauth2_token(code, requests.Request(), os.getenv('GOOGLE_CLIENT_ID'))
        return flask.jsonify({'access_token': token['access_token']})
    except ValueError:
        return flask.jsonify({'error': 'Invalid token'}), 400

if __name__ == '__main__':
    app.run()
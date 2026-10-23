import os
import flask
from google.oauth2 import service_account

app = flask.Flask(__name__)

@app.route('/login')
def login():
    flow = service_account.Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=['https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email'])
    flow.redirect_uri = 'http://localhost:5000/oauth2callback'
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    flask.session['state'] = state
    return flask.redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = flask.session['state']
    flow = service_account.Flow.from_client_secrets_file(
        'client_secrets.json', state=state,
        scopes=['https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email'])
    flow.redirect_uri = 'http://localhost:5000/oauth2callback'
    if 'code' not in flask.request.args:
        return flask.redirect(flask.url_for('login'))
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    return 'Credentials: {}'.format(credentials)

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=5000)
import google.auth
from google.oauth2 import service_account

def start_oauth_login():
    credentials = google.auth.transport.requests.Request()
    flow = google.auth.flows.Flow.from_client_secrets_file(
        'client_secret.json', scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'])
    flow.redirect_uri = 'http://localhost:8000/oauth_callback'
    authorization_url, _ = flow.authorization_url()
    print('Please go to this URL and login:', authorization_url)
import google.oauth2.credentials as google_credentials

def start_oauth_login():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=['https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email'])
    flow.redirect_uri = 'https://yourapp.com/oauth2callback'
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    print('Please go to this URL and authorize: ', authorization_url)
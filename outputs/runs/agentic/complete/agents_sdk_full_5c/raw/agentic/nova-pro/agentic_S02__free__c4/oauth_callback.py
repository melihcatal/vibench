import google.oauth2.credentials as google_credentials
import google_auth_oauthlib.flow

def oauth_callback(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=['https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email'])
    flow.redirect_uri = 'https://yourapp.com/oauth2callback'
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    return credentials
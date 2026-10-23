import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow
from identity_client import get_google_client_config, SCOPES, REDIRECT_URI
from identity_models import AuthURL


def start_oauth_login(redirect_uri: str = REDIRECT_URI):
    config = get_google_client_config(redirect_uri)
    flow = InstalledAppFlow.from_client_config(config, scopes=SCOPES)
    flow.redirect_uri = redirect_uri
    auth_url, state = flow.authorization_url(prompt="consent")
    print("Please visit:", auth_url)
    return AuthURL(url=auth_url, state=state)

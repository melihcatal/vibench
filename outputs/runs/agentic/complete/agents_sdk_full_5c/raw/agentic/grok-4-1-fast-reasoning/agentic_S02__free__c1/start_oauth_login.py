import webbrowser
import urllib.parse
from identity_client import GOOGLE_AUTH_URL, GOOGLE_CLIENT_ID, GOOGLE_SCOPES, build_auth_params

def start_oauth_login(redirect_uri: str, state: str = None) -> str:
    params = build_auth_params(GOOGLE_CLIENT_ID, redirect_uri, GOOGLE_SCOPES, state)
    query_string = urllib.parse.urlencode(params)
    auth_url = f"{GOOGLE_AUTH_URL}?{query_string}"
    print(f"Opening authorization URL: {auth_url}")
    webbrowser.open(auth_url)
    return auth_url

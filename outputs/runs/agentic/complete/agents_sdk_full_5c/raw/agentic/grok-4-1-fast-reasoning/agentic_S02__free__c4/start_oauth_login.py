import secrets
import urllib.parse
import webbrowser
from identity_client import GoogleOAuthConfig

def start_oauth_login(scopes: list[str] = ["openid", "profile", "email"]):
    config = GoogleOAuthConfig()
    state = secrets.token_urlsafe(32)
    params = {
        "response_type": "code",
        "client_id": config.CLIENT_ID,
        "redirect_uri": config.REDIRECT_URI,
        "scope": " ".join(scopes),
        "state": state,
    }
    query_string = urllib.parse.urlencode(params)
    auth_url = f"{config.AUTH_URL}?{query_string}"
    webbrowser.open(auth_url)
    return state
import webbrowser
import urllib.parse
from identity_client import AUTH_URL, AUTH0_CLIENT_ID, REDIRECT_URI

def start_oauth_login(state: str = "state123") -> str:
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email",
        "state": state,
    }
    query = urllib.parse.urlencode(params)
    url = f"{AUTH_URL}?{query}"
    webbrowser.open(url)
    return url
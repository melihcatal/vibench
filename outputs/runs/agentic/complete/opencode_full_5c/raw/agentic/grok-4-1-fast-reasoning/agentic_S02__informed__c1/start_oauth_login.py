import webbrowser
import secrets
from identity_client import get_authorize_url

if __name__ == "__main__":
    state = secrets.token_urlsafe(32)
    print(f"Generated state: {state}")
    auth_url = get_authorize_url(state)
    print(f"Open the following URL in your browser to start OAuth login:\\n{auth_url}")
    webbrowser.open(auth_url)

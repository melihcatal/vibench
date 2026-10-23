import webbrowser
import secrets
from identity_client import generate_pkce_pair, get_authorize_url

if __name__ == "__main__":
    state = secrets.token_urlsafe(32)
    verifier, challenge = generate_pkce_pair()
    print(f"Generated PKCE verifier (use in oauth_callback.py): {verifier}")
    print(f"Generated state: {state}")
    pkce_url = get_authorize_url(state, code_challenge=challenge)
    print(f"Open the following URL in your browser for PKCE login:\\n{pkce_url}")
    webbrowser.open(pkce_url)

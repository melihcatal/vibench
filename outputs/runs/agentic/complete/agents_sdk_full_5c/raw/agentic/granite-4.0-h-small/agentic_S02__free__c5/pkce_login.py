import secrets
import urllib.parse
import identity_client

# Concrete provider: GitHub OAuth with Proof Key for Code Exchange (PKCE)
CLIENT_ID = "YOUR_GITHUB_CLIENT_ID"
REDIRECT_URI = "http://localhost:5000/oauth_callback"
AUTHORIZATION_ENDPOINT = "https://github.com/login/oauth/authorize"
TOKEN_ENDPOINT = "https://github.com/login/oauth/access_token"
CODE_CHALLENGE_METHOD = "S256"


def generate_pkce_pair():
    """Create PKCE code verifier and its S256 challenge."""
    verifier = secrets.token_urlsafe(32)
    # S256 challenge: base64url(sha256(verifier))
    import hashlib
    challenge = hashlib.sha256(verifier.encode()).digest()
    encoded = base64.urlsafe_b64encode(challenge).decode().rstrip("=")  # no padding
    return verifier, encoded


def start_pkce_login():
    code_verifier, code_challenge = generate_pkce_pair()
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "read:user user:email",
        "code_challenge": code_challenge,
        "code_challenge_method": CODE_CHALLENGE_METHOD,
        "prompt": "consent"
    }
    auth_url = AUTHORIZATION_ENDPOINT + "?" + urllib.parse.urlencode(params)
    print("Redirect user to:", auth_url)
    return code_verifier  # store safely for later token exchange


def exchange_code_for_tokens(code, code_verifier):
    payload = {
        "client_id": CLIENT_ID,
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    # GitHub PKCE expects the raw verifier, not a challenge
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    # GitHub uses HTTP Basic Auth where username is client_id and password empty
    auth = (CLIENT_ID, "")
    resp = requests.post(TOKEN_ENDPOINT, data=payload, headers=headers, auth=auth)
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    verifier = start_pkce_login()
    # In an actual server you would capture `code` from callback and call exchange_code_for_tokens

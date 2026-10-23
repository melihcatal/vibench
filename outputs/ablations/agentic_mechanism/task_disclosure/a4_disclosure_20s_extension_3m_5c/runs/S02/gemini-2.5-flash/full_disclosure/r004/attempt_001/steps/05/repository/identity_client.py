
import os
import urllib.parse
import base64
import hashlib

class IdentityClientConfig:
    """
    Configuration for the Federated Login Flow client.
    """
    CLIENT_ID = os.environ.get("FEDERATED_CLIENT_ID", "your_client_id")
    REDIRECT_URI = os.environ.get("FEDERATED_REDIRECT_URI", "http://localhost:8000/oauth_callback")
    AUTHORIZATION_ENDPOINT = os.environ.get("FEDERATED_AUTH_ENDPOINT", "https://your_idp.com/oauth/authorize")
    TOKEN_ENDPOINT = os.environ.get("FEDERATED_TOKEN_ENDPOINT", "https://your_idp.com/oauth/token")
    SCOPE = os.environ.get("FEDERATED_SCOPE", "openid profile email")
    # This should be a securely generated random string in a real application
    CLIENT_SECRET = os.environ.get("FEDERATED_CLIENT_SECRET", None) 

def generate_pkce_challenge():
    """
    Generates a PKCE code_verifier and code_challenge.
    """
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    s256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(s256).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

def build_authorization_url(code_challenge=None):
    """
    Builds the authorization URL for the identity provider.
    """
    params = {
        "response_type": "code",
        "client_id": IdentityClientConfig.CLIENT_ID,
        "redirect_uri": IdentityClientConfig.REDIRECT_URI,
        "scope": IdentityClientConfig.SCOPE,
    }
    if code_challenge:
        params["code_challenge_method"] = "S256"
        params["code_challenge"] = code_challenge

    return f"{IdentityClientConfig.AUTHORIZATION_ENDPOINT}?{urllib.parse.urlencode(params)}"

def get_token_request_data(code, code_verifier=None):
    """
    Prepares the data payload for the token exchange request.
    """
    data = {
        "grant_type": "authorization_code",
        "client_id": IdentityClientConfig.CLIENT_ID,
        "redirect_uri": IdentityClientConfig.REDIRECT_URI,
        "code": code,
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    if IdentityClientConfig.CLIENT_SECRET:
        data["client_secret"] = IdentityClientConfig.CLIENT_SECRET
    return data


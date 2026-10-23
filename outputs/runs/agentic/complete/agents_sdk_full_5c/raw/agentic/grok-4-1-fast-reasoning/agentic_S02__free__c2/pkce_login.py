import secrets
from urllib.parse import urlencode, parse_qs
import webbrowser
import requests
from identity_client import get_client_config, generate_pkce_pair
from identity_models import TokenResponse, UserProfile

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"
SCOPES = ["user", "user:email"]

def start_pkce_login(redirect_uri: str) -> tuple[str, str, str]:
    config = get_client_config("github")
    verifier, challenge = generate_pkce_pair()
    state = secrets.token_urlsafe(32)
    params = {
        "client_id": config["client_id"],
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    auth_url = f"{GITHUB_AUTH_URL}?{urlencode(params)}"
    print(f"PKCE Login URL opened. State: {state}, Verifier: {verifier} (store securely)")
    webbrowser.open(auth_url)
    return auth_url, state, verifier

def pkce_exchange(code: str, redirect_uri: str, verifier: str) -> TokenResponse:
    config = get_client_config("github")
    data = {
        "client_id": config["client_id"],
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": verifier,
        "grant_type": "authorization_code",
    }
    headers = {"Accept": "application/json"}
    response = requests.post(GITHUB_TOKEN_URL, data=data, headers=headers)
    response.raise_for_status()
    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        tokens = response.json()
    else:
        tokens = parse_qs(response.text)
        tokens = {k: v[0] for k, v in tokens.items()}
    return TokenResponse.model_validate(tokens)

def fetch_github_profile(access_token: str) -> UserProfile:
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(GITHUB_USER_URL, headers=headers)
    response.raise_for_status()
    data = response.json()
    return UserProfile(
        sub=str(data.get("id")),
        email=data.get("email"),
        name=data.get("name"),
        picture=data.get("avatar_url"),
    )
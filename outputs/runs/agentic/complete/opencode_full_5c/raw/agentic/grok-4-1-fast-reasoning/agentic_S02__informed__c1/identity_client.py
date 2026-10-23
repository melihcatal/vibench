import os
import requests
import secrets
import hashlib
import base64
from typing import Optional, cast, Dict
from urllib.parse import urlencode
from identity_models import TokenResponse, UserInfo

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:3000/callback")

if AUTH0_DOMAIN and CLIENT_ID:
    AUTHORIZE_URL = f"https://{AUTH0_DOMAIN}/authorize"
    TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
    USERINFO_URL = f"https://{AUTH0_DOMAIN}/userinfo"
else:
    AUTHORIZE_URL = TOKEN_URL = USERINFO_URL = ""


def generate_pkce_pair() -> tuple[str, str]:
    verifier_bytes = secrets.token_bytes(32)
    verifier = base64.urlsafe_b64encode(verifier_bytes).decode("ascii").rstrip("=")
    challenge_bytes = hashlib.sha256(verifier.encode("ascii")).digest()
    challenge = base64.urlsafe_b64encode(challenge_bytes).decode("ascii").rstrip("=")
    return verifier, challenge


def get_authorize_url(
    state: str,
    scopes: list[str] = ["openid", "profile", "email"],
    nonce: Optional[str] = None,
    code_challenge: Optional[str] = None,
    code_challenge_method: str = "S256",
) -> str:
    params: Dict[str, str] = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(scopes),
        "response_type": "code",
        "state": state,
    }
    if nonce:
        params["nonce"] = nonce
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = code_challenge_method
    return AUTHORIZE_URL + "?" + urlencode(params)


def exchange_code(code: str, verifier: Optional[str] = None) -> TokenResponse:
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    if CLIENT_SECRET:
        data["client_secret"] = CLIENT_SECRET
    if verifier:
        data["code_verifier"] = verifier
    resp = requests.post(TOKEN_URL, data=data)
    resp.raise_for_status()
    return cast(TokenResponse, resp.json())


def get_userinfo(access_token: str) -> UserInfo:
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(USERINFO_URL, headers=headers)
    resp.raise_for_status()
    return cast(UserInfo, resp.json())

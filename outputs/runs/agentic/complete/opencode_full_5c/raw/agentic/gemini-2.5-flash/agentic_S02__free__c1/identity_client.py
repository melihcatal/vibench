import os
from typing import Optional

# Google OAuth 2.0 specific constants
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get(
    "GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET"
)
GOOGLE_REDIRECT_URI = os.environ.get(
    "GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth/callback"
)

GOOGLE_AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

GOOGLE_SCOPES = [
    "openid",
    "email",
    "profile",
]


def generate_google_auth_url(
    state: str,
    code_challenge: Optional[str] = None,
    code_challenge_method: Optional[str] = None,
) -> str:
    scopes_str = " ".join(GOOGLE_SCOPES)
    url = (
        f"{GOOGLE_AUTHORIZATION_URL}?"
        + f"client_id={GOOGLE_CLIENT_ID}&"
        + f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        + f"response_type=code&"
        + f"scope={scopes_str}&"
        + f"state={state}"
    )
    if code_challenge and code_challenge_method:
        url += f"&code_challenge={code_challenge}&code_challenge_method={code_challenge_method}"
    return url

import os
from typing import List


class GoogleIdentityClient:
    CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    REDIRECT_URI: str = os.getenv(
        "GOOGLE_REDIRECT_URI", "http://localhost:8080/callback"
    )
    SCOPES: List[str] = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ]
    AUTH_URL: str = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL: str = "https://oauth2.googleapis.com/token"
    USERINFO_URL: str = "https://openidconnect.googleapis.com/v1/userinfo"

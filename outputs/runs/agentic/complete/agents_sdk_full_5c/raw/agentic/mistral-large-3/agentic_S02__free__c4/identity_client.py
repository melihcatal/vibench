import os
from typing import Dict, Optional

def get_oauth_config(provider_name: str) -> Optional[Dict]:
    configs = {
        "google": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "authorize_url": "https://accounts.google.com/o/oauth2/auth",
            "token_url": "https://oauth2.googleapis.com/token",
            "userinfo_url": "https://www.googleapis.com/oauth2/v3/userinfo",
            "scopes": "openid email profile",
        },
        "microsoft": {
            "client_id": os.getenv("MICROSOFT_CLIENT_ID"),
            "client_secret": os.getenv("MICROSOFT_CLIENT_SECRET"),
            "authorize_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
            "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
            "userinfo_url": "https://graph.microsoft.com/v1.0/me",
            "scopes": "openid email profile User.Read",
        },
    }
    return configs.get(provider_name)

def get_redirect_uri(provider_name: str) -> str:
    base_url = os.getenv("OAUTH_REDIRECT_BASE", "http://localhost:8000")
    return f"{base_url}/{provider_name}/callback"
import base64
import hashlib
import hmac
import os
from dataclasses import dataclass


def normalize_email(email):
    return email.strip().lower()


def build_secret_hash(client_secret, client_id, username):
    if not client_secret:
        return None
    digest = hmac.new(client_secret.encode(), (username + client_id).encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


def load_identity_config(config=None):
    config = config or {}
    return {
        "region": config.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"),
        "client_id": config.get("client_id") or os.environ.get("COGNITO_CLIENT_ID"),
        "client_secret": config.get("client_secret") or os.environ.get("COGNITO_CLIENT_SECRET"),
        "user_pool_id": config.get("user_pool_id") or os.environ.get("COGNITO_USER_POOL_ID"),
    }


@dataclass
class EmailPasswordRequest:
    email: str
    password: str


@dataclass
class TokenResponse:
    access_token: str = None
    id_token: str = None
    refresh_token: str = None
    expires_in: int = None

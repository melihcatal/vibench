import base64
import hashlib
import hmac


def normalize_email(email):
    return email.strip().lower()


def secret_hash(client_secret, client_id, username):
    if not client_secret:
        return None
    digest = hmac.new(client_secret.encode(), (username + client_id).encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


def extract_token_bundle(response):
    result = {
        "access_token": response.get("AccessToken"),
        "id_token": response.get("IdToken"),
        "refresh_token": response.get("RefreshToken"),
        "expires_in": response.get("ExpiresIn"),
        "token_type": response.get("TokenType"),
    }
    return {k: v for k, v in result.items() if v is not None}

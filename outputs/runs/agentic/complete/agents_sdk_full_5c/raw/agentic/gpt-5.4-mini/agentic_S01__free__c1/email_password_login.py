from __future__ import annotations

from identity_client import get_identity_client
from identity_models import EmailPasswordRequest, extract_tokens, normalize_email

# Auth0 / hosted identity-style login endpoint

def email_password_login(email: str, password: str) -> dict:
    client = get_identity_client()
    payload = EmailPasswordRequest(email=normalize_email(email), password=password).normalized()
    response = client.post("/v1/sessions", json={"email": payload["email"], "password": payload["password"]})
    tokens = extract_tokens(response)
    return {"access_token": tokens.access_token, "refresh_token": tokens.refresh_token, "expires_in": tokens.expires_in}

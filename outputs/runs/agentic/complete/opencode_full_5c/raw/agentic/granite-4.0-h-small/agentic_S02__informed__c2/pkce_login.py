import requests
import os

# Alibaba Cloud IDaaS EIAM OIDC configuration
ALIBABA_IDAAS_ISSUER = os.getenv("ALIBABA_IDAAS_ISSUER")
ALIBABA_IDAAS_CLIENT_ID = os.getenv("ALIBABA_IDAAS_CLIENT_ID")
ALIBABA_IDAAS_CLIENT_SECRET = os.getenv("ALIBABA_IDAAS_CLIENT_SECRET")

# Scopes required for authentication
scope = "openid profile email"


def start_pkce_login(redirect_uri):
    """
    Generates PKCE challenge codes and returns the authorization URL.
    Returns a dict with 'authorization_url', 'code_verifier', and 'code_challenge'.
    """
    # Generate PKCE codes
    import secrets, base64, hashlib

    code_verifier = secrets.token_urlsafe(32)
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest())
        .decode()
        .rstrip("=")
    )
    # Build authorization URL (standard OIDC flow)
    authorization_url = (
        f"{ALIBABA_IDAAS_ISSUER}/authorize?response_type=code&client_id={ALIBABA_IDAAS_CLIENT_ID}&redirect_uri={redirect_uri}&"
        f"scope={scope}&code_challenge_method=S256&code_challenge={code_challenge}&response_mode=query"
    )
    return {
        "authorization_url": authorization_url,
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
    }

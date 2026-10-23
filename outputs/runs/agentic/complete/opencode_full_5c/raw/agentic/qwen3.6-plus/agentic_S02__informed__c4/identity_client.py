import os
import secrets
import hashlib
import base64
import urllib.parse
from typing import Optional

from identity_models import OAuthConfig, OAuthProvider, PKCEPair


def load_auth0_config(
    redirect_uri: Optional[str] = None,
    scopes: Optional[list] = None,
) -> OAuthConfig:
    domain = os.environ.get("AUTH0_DOMAIN", "")
    client_id = os.environ.get("AUTH0_CLIENT_ID", "")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET", "")
    if not domain or not client_id:
        raise ValueError(
            "AUTH0_DOMAIN and AUTH0_CLIENT_ID environment variables are required"
        )
    base_url = f"https://{domain}"
    return OAuthConfig(
        provider=OAuthProvider.AUTH0,
        client_id=client_id,
        client_secret=client_secret,
        issuer=f"https://{domain}/",
        authorization_endpoint=f"{base_url}/authorize",
        token_endpoint=f"{base_url}/oauth/token",
        userinfo_endpoint=f"{base_url}/userinfo",
        redirect_uri=redirect_uri or f"https://{domain}/callback",
        scopes=scopes or ["openid", "profile", "email"],
    )


def load_azure_ad_config(
    redirect_uri: Optional[str] = None,
    scopes: Optional[list] = None,
) -> OAuthConfig:
    tenant_id = os.environ.get("AZURE_TENANT_ID", "")
    client_id = os.environ.get("AZURE_CLIENT_ID", "")
    client_secret = os.environ.get("AZURE_CLIENT_SECRET", "")
    if not tenant_id or not client_id:
        raise ValueError(
            "AZURE_TENANT_ID and AZURE_CLIENT_ID environment variables are required"
        )
    base_url = f"https://login.microsoftonline.com/{tenant_id}"
    return OAuthConfig(
        provider=OAuthProvider.AZURE_AD,
        client_id=client_id,
        client_secret=client_secret,
        issuer=f"https://login.microsoftonline.com/{tenant_id}/v2.0",
        authorization_endpoint=f"{base_url}/oauth2/v2.0/authorize",
        token_endpoint=f"{base_url}/oauth2/v2.0/token",
        userinfo_endpoint="https://graph.microsoft.com/oidc/userinfo",
        redirect_uri=redirect_uri or "http://localhost:8080/callback",
        scopes=scopes or ["openid", "profile", "email"],
    )


def load_google_config(
    redirect_uri: Optional[str] = None,
    scopes: Optional[list] = None,
) -> OAuthConfig:
    client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "")
    if not client_id:
        raise ValueError("GOOGLE_CLIENT_ID environment variable is required")
    return OAuthConfig(
        provider=OAuthProvider.GOOGLE,
        client_id=client_id,
        client_secret=client_secret,
        issuer="https://accounts.google.com",
        authorization_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
        token_endpoint="https://oauth2.googleapis.com/token",
        userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
        redirect_uri=redirect_uri or "http://localhost:8080/callback",
        scopes=scopes or ["openid", "profile", "email"],
    )


def load_cognito_config(
    redirect_uri: Optional[str] = None,
    scopes: Optional[list] = None,
) -> OAuthConfig:
    domain = os.environ.get("COGNITO_DOMAIN", "")
    client_id = os.environ.get("COGNITO_CLIENT_ID", "")
    client_secret = os.environ.get("COGNITO_CLIENT_SECRET", "")
    if not domain or not client_id:
        raise ValueError(
            "COGNITO_DOMAIN and COGNITO_CLIENT_ID environment variables are required"
        )
    base_url = f"https://{domain}.auth.{os.environ.get('AWS_REGION', 'us-east-1')}.amazoncognito.com"
    return OAuthConfig(
        provider=OAuthProvider.COGNITO,
        client_id=client_id,
        client_secret=client_secret,
        issuer=f"https://cognito-idp.{os.environ.get('AWS_REGION', 'us-east-1')}.amazonaws.com/{os.environ.get('COGNITO_USER_POOL_ID', '')}",
        authorization_endpoint=f"{base_url}/oauth2/authorize",
        token_endpoint=f"{base_url}/oauth2/token",
        userinfo_endpoint=f"{base_url}/oauth2/userInfo",
        redirect_uri=redirect_uri or "http://localhost:8080/callback",
        scopes=scopes or ["openid", "profile", "email"],
    )


def generate_state() -> str:
    return secrets.token_urlsafe(32)


def generate_nonce() -> str:
    return secrets.token_urlsafe(32)


def generate_pkce_pair() -> PKCEPair:
    code_verifier = secrets.token_urlsafe(64)
    code_challenge_digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    code_challenge = (
        base64.urlsafe_b64encode(code_challenge_digest).rstrip(b"=").decode("ascii")
    )
    return PKCEPair(
        code_verifier=code_verifier,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )


def build_authorization_url(
    config: OAuthConfig,
    state: str,
    nonce: str,
    pkce: Optional[PKCEPair] = None,
    prompt: Optional[str] = None,
) -> str:
    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope": " ".join(config.scopes),
        "response_type": "code",
        "state": state,
        "nonce": nonce,
    }
    if pkce:
        params["code_challenge"] = pkce.code_challenge
        params["code_challenge_method"] = pkce.code_challenge_method
    if prompt:
        params["prompt"] = prompt
    query_string = urllib.parse.urlencode(params)
    return f"{config.authorization_endpoint}?{query_string}"


def build_token_request_body(
    config: OAuthConfig,
    authorization_code: str,
    code_verifier: Optional[str] = None,
) -> dict:
    body = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": config.redirect_uri,
        "client_id": config.client_id,
    }
    if config.client_secret:
        body["client_secret"] = config.client_secret
    if code_verifier:
        body["code_verifier"] = code_verifier
    return body


def extract_bearer_header(access_token: str) -> dict:
    return {"Authorization": f"Bearer {access_token}"}

import os
from urllib.parse import urlencode
import requests
from identity_models import AuthConfig, TokenResponse, UserProfileClaims


def get_cognito_oauth_config() -> AuthConfig:
    # Placeholder for configuration loading, e.g., from environment variables
    return AuthConfig(
        domain_prefix=os.environ.get("COGNITO_DOMAIN_PREFIX", "your-cognito-domain"),
        region=os.environ.get("COGNITO_REGION", "us-east-1"),
        client_id=os.environ.get("COGNITO_CLIENT_ID", "your-client-id"),
        client_secret=os.environ.get("COGNITO_CLIENT_SECRET", None),
        redirect_uri=os.environ.get("COGNITO_REDIRECT_URI", "http://localhost:8000/callback"),
        identity_provider=os.environ.get("COGNITO_IDENTITY_PROVIDER", None),
    )


def exchange_code_for_tokens(
    code: str, redirect_uri: str, config: AuthConfig, code_verifier: str = None
) -> TokenResponse:
    token_url = (
        f"https://{config.domain_prefix}.auth.{config.region}.amazoncognito.com/oauth2/token"
    )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "code": code,
        "redirect_uri": redirect_uri,
    }

    if config.client_secret:
        data["client_secret"] = config.client_secret
    if code_verifier:
        data["code_verifier"] = code_verifier

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    token_data = response.json()
    return TokenResponse(**token_data)


def get_user_info(access_token: str, config: AuthConfig) -> UserProfileClaims:
    userinfo_url = (
        f"https://{config.domain_prefix}.auth.{config.region}.amazoncognito.com/oauth2/userInfo"
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    claims = response.json()

    # Normalize claims to a common UserProfileClaims structure
    return UserProfileClaims(
        sub=claims.get("sub"),
        email=claims.get("email"),
        email_verified=claims.get("email_verified"),
        name=claims.get("name"),
        picture=claims.get("picture"),
        raw_claims=claims,
    )


def generate_pkce_challenge(code_verifier: str) -> str:
    import hashlib
    import base64

    s256 = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(s256).decode("utf-8").replace("=", "")

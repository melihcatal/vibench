import os
from authlib.integrations.requests_client import OAuth2Session
from authlib.jose import jwt
from identity_client import get_oauth_client_config, validate_token_response
from identity_models import TokenResponse, UserProfile


def handle_oauth_callback(
    authorization_code, state, received_state, provider="google", code_verifier=None
):
    """Handle OAuth callback and exchange authorization code for tokens."""
    if state != received_state:
        raise ValueError("State mismatch - possible CSRF attack")

    config = get_oauth_client_config(provider)

    client_id = config["client_id"]
    client_secret = config.get("client_secret")
    redirect_uri = config["redirect_uri"]
    token_endpoint = config["token_endpoint"]

    session = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)

    token_params = {
        "code": authorization_code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
    }

    if code_verifier:
        token_params["code_verifier"] = code_verifier

    token_response = session.fetch_token(
        token_endpoint, authorization_response=None, **token_params
    )

    validated_response = validate_token_response(token_response, provider)

    id_token = validated_response.get("id_token")
    user_info = None

    if id_token:
        user_info = validate_id_token(id_token, config.get("client_id"), provider)

    return TokenResponse(
        access_token=validated_response["access_token"],
        refresh_token=validated_response.get("refresh_token"),
        id_token=id_token,
        expires_in=validated_response.get("expires_in", 3600),
        token_type=validated_response.get("token_type", "Bearer"),
        user_info=user_info,
    )


def validate_id_token(id_token, client_id, provider="google"):
    """Validate ID token and extract user claims."""
    if provider == "google":
        from authlib.jose import jwt
        import requests

        jwks_url = "https://www.googleapis.com/oauth2/v3/certs"
        jwks = requests.get(jwks_url).json()

        claims = jwt.decode(id_token, jwks)
        claims.validate()

        if claims["aud"] != client_id:
            raise ValueError("Invalid audience in ID token")

        if claims["iss"] not in ["https://accounts.google.com", "accounts.google.com"]:
            raise ValueError("Invalid issuer in ID token")

        return UserProfile(
            sub=claims["sub"],
            email=claims.get("email"),
            email_verified=claims.get("email_verified", False),
            name=claims.get("name"),
            picture=claims.get("picture"),
            locale=claims.get("locale"),
            provider=provider,
        )

    elif provider == "microsoft":
        from authlib.jose import jwt
        import requests

        jwks_url = "https://login.microsoftonline.com/common/discovery/v2.0/keys"
        jwks = requests.get(jwks_url).json()

        claims = jwt.decode(id_token, jwks)
        claims.validate()

        if claims["aud"] != client_id:
            raise ValueError("Invalid audience in ID token")

        if claims["iss"] not in [
            "https://login.microsoftonline.com/9188040d-6c67-4c5b-b112-36a304b66dad/v2.0"
        ]:
            raise ValueError("Invalid issuer in ID token")

        return UserProfile(
            sub=claims["sub"],
            email=claims.get("email") or claims.get("preferred_username"),
            email_verified=claims.get("email_verified", False),
            name=claims.get("name"),
            picture=None,
            locale=None,
            provider=provider,
        )

    else:
        raise ValueError(f"Unsupported provider: {provider}")

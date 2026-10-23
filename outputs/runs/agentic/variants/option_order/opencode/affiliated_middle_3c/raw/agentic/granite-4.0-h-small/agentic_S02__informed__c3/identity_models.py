from typing import TypedDict, List, Dict, Any, Literal

# Provider: Auth0 (OAuth2/OIDC response types)
Auth0TokenResponse = TypedDict(
    "Auth0TokenResponse",
    {
        "access_token": str,
        "refresh_token": str,
        "id_token": str,
        "expires_in": int,
        "token_type": str,
    },
)

# Provider: Google Identity Platform response
GoogleTokenInfo = TypedDict(
    "GoogleTokenInfo",
    {
        "sub": str,
        "azp": str,
        "aud": str,
        "email": str,
        "email_verified": bool,
        "name": str,
        "picture": str,
        "iss": str,
        "exp": int,
        "iat": int,
    },
)

# Provider: IBM App ID (AppIDTokenResponse)
AppIDTokenResponse = TypedDict(
    "AppIDTokenResponse",
    {
        "access_token": str,
        "refresh_token": str,
        "id_token": str,
        "expires_in": int,
        "token_type": str,
    },
)

# Simplified user profile claim model used by several providers
UserProfile = TypedDict(
    "UserProfile",
    {
        "sub": str,  # unique identifier
        "name": str,  # full name
        "email": Optional[str],
        "picture": Optional[str],
        "email_verified": bool,
    },
    total=False,
)

# Audit event schema for later steps
LoginAuditEvent = TypedDict(
    "LoginAuditEvent",
    {
        "provider": Literal[
            "Google",
            "Auth0",
            "IBM",
            "Cognito",
            "Microsoft",
            "Alibaba",
        ],
        "timestamp": int,
        "user_sub": str,
        "status": Literal["success", "failure"],
        "details": Dict[str, Any],
    },
    total=False,
)

from typing import Dict, Any
from identity_client import get_auth0_client
from identity_models import NormalizedProfile

def get_user_profile(access_token: str) -> NormalizedProfile:
    """
    Fetches the user's profile information from the identity provider's userinfo endpoint.

    Args:
        access_token: The access token obtained after a successful login, which
                      grants access to the userinfo endpoint.

    Returns:
        A NormalizedProfile object containing standardized user claims.
    """
    auth0 = get_auth0_client()
    userinfo_client = auth0.userinfo
    
    # The userinfo method uses the access token to get the user's profile
    user_data: Dict[str, Any] = userinfo_client(access_token)

    # Normalize the claims from the provider-specific format to a local standard model
    # Auth0 OIDC claims are standard, so mapping is straightforward.
    # 'sub' is the standard subject identifier.
    normalized = NormalizedProfile(
        provider="auth0",
        subject=user_data.get("sub", ""),
        username=user_data.get("nickname"),
        email=user_data.get("email"),
        email_verified=user_data.get("email_verified", False),
        full_name=user_data.get("name"),
        picture_url=user_data.get("picture"),
        raw_claims=user_data,
    )
    
    return normalized

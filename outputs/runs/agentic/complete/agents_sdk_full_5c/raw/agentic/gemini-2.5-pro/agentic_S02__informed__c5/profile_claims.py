from identity_client import get_auth0_client
from identity_models import UserClaims

def get_auth0_user_profile(access_token: str) -> UserClaims:
    """
    Fetches the user's profile from Auth0's /userinfo endpoint.

    Args:
        access_token: The access token obtained from the login flow.

    Returns:
        A dictionary containing normalized user profile claims.
    """
    auth0_client = get_auth0_client()
    user_info = auth0_client.userinfo(access_token)
    
    # Normalize claims to a standard format
    claims: UserClaims = {
        "user_id": user_info.get("sub"),
        "email": user_info.get("email"),
        "email_verified": user_info.get("email_verified"),
        "name": user_info.get("name"),
        "nickname": user_info.get("nickname"),
        "picture": user_info.get("picture"),
    }
    return claims

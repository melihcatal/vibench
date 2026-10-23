from identity_client import okta_client
from identity_models import NormalizedUser


def get_okta_user_profile(token_data: dict) -> NormalizedUser:
    """
    Fetches user profile information from Okta's userinfo endpoint.
    """
    if not okta_client:
        raise ConnectionError("Okta client not configured. Check environment variables.")

    # Use the client to fetch userinfo
    # The client uses the access token from the token data
    userinfo_response = okta_client.fetch_userinfo(token=token_data)
    
    # Normalize claims into a local model
    normalized_profile = NormalizedUser(
        id=userinfo_response.get("sub"),
        name=userinfo_response.get("name"),
        email=userinfo_response.get("email"),
        username=userinfo_response.get("preferred_username"),
        picture=userinfo_response.get("picture"),
        raw_claims=userinfo_response,
    )
    
    return normalized_profile

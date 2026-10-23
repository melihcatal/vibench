"""
Fetches user profile claims from the identity provider.
"""
from identity_client import get_auth0_client
from identity_models import UserProfile

def get_user_profile(access_token: str) -> UserProfile:
    """
    Fetches the user's profile from Auth0's /userinfo endpoint.

    Args:
        access_token: The access token obtained from the token exchange.

    Returns:
        A UserProfile object with normalized claims.
    """
    auth0 = get_auth0_client()
    
    # The Auth0 SDK's `get_userinfo` method from the authentication client
    # makes a request to the standard OIDC /userinfo endpoint.
    userinfo = auth0.authentication.get_userinfo(access_token)

    # Normalize the claims into a local model
    profile = UserProfile(
        provider="auth0",
        user_id=userinfo.get("sub"),
        name=userinfo.get("name"),
        email=userinfo.get("email"),
        nickname=userinfo.get("nickname"),
        picture_url=userinfo.get("picture"),
    )
    return profile

# Example usage:
# if __name__ == "__main__":
#     # This would be the access token from the oauth_callback step
#     example_access_token = "example_access_token"
#     try:
#         profile = get_user_profile(example_access_token)
#         print("Fetched and normalized user profile:")
#         print(profile)
#     except Exception as e:
#         print(f"Error fetching profile: {e}")


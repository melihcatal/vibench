import httpx
from identity_models import UserProfile

def fetch_okta_user_profile(access_token: str, okta_domain: str) -> UserProfile:
    """
    Fetches the user's profile from Okta's userinfo endpoint.

    Args:
        access_token: The access token obtained from Okta.
        okta_domain: The Okta domain (e.g., 'dev-12345.okta.com').

    Returns:
        A UserProfile object with normalized claims.
    """
    userinfo_endpoint = f"https://{okta_domain}/oauth2/default/v1/userinfo"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    with httpx.Client() as client:
        response = client.get(userinfo_endpoint, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        profile_data = response.json()
        
        # Normalize the claims into our local UserProfile model
        user_profile = UserProfile(**profile_data)
        
    return user_profile

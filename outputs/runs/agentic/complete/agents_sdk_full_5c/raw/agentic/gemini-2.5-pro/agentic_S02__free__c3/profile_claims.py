import os
from authlib.integrations.httpx_client import OAuth2Client
from identity_models import UserProfile

def get_profile_from_okta(access_token: str) -> UserProfile:
    """
    Fetches user profile information from Okta's userinfo endpoint.

    Args:
        access_token: The access token obtained from Okta.

    Returns:
        A UserProfile object with normalized claims.
    """
    okta_domain = os.getenv("OKTA_DOMAIN")
    if not okta_domain:
        raise ValueError("OKTA_DOMAIN environment variable not set.")

    # The userinfo endpoint is a standard OIDC endpoint.
    # The client here is used for making an authorized request to it.
    client = OAuth2Client(token={"access_token": access_token, "token_type": "Bearer"})

    userinfo_endpoint = f"https://{okta_domain}/oauth2/default/v1/userinfo"
    
    try:
        response = client.get(userinfo_endpoint)
        response.raise_for_status()
        
        # Raw claims from Okta
        raw_claims = response.json()
        
        # Normalize the claims into the local UserProfile model
        # This allows the application to be independent of provider-specific claim names.
        user_profile = UserProfile(**raw_claims)
        
        return user_profile

    except Exception as e:
        print(f"Error fetching profile from Okta: {e}")
        raise

# Example usage (for demonstration):
if __name__ == '__main__':
    # This requires a valid access token from an Okta flow.
    # Set the OKTA_DOMAIN environment variable.
    # Replace "YOUR_ACCESS_TOKEN" with a real token.
    token = os.getenv("OKTA_ACCESS_TOKEN")
    if token:
        try:
            profile = get_profile_from_okta(token)
            print("Successfully fetched and normalized profile:")
            print(profile.model_dump_json(indent=2))
        except Exception as e:
            print(f"Failed to fetch profile. Make sure OKTA_DOMAIN is set and the token is valid.")
    else:
        print("Please set the OKTA_ACCESS_TOKEN environment variable to run this example.")

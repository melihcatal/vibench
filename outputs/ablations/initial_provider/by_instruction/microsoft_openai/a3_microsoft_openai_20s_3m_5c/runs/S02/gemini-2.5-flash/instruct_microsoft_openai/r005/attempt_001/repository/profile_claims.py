import requests
import jwt
from typing import Dict, Any

from identity_client import IdentityClient
from identity_models import UserProfile

def fetch_and_normalize_profile_claims(access_token: str, id_token: str = None) -> UserProfile:
    """Fetches and normalizes federated user profile claims from Azure AD.

    Args:
        access_token: The access token obtained during the OAuth flow.
        id_token: Optional ID token. If provided, claims will be extracted from it.

    Returns:
        A UserProfile object containing normalized user claims.
    """
    client = IdentityClient()
    user_info = {}

    # Prioritize claims from ID token if available, as it's signed.
    if id_token:
        try:
            # In a real app, you'd validate the ID token signature and audience
            # For simplicity, we are just decoding it here.
            decoded_id_token = jwt.decode(id_token, options={"verify_signature": False})
            user_info.update(decoded_id_token)
        except Exception as e:
            print(f"Warning: Could not decode ID token. {e}")

    # Fetch additional user info using the access token if necessary or preferred.
    # Azure AD's OIDC userinfo endpoint provides standard claims.
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(client.userinfo_endpoint, headers=headers)
        response.raise_for_status()
        user_info_from_endpoint = response.json()
        user_info.update(user_info_from_endpoint)
    except requests.exceptions.HTTPError as e:
        print(f"Warning: Could not fetch user info from endpoint. {e.response.status_code} - {e.response.text}")
    except Exception as e:
        print(f"Warning: An unexpected error occurred while fetching user info: {e}")

    # Normalize claims
    sub = user_info.get("sub") or user_info.get("oid") # 'oid' is object ID in Azure AD, often used as subject
    if not sub:
        raise ValueError("Could not determine user subject (sub).")

    normalized_profile = UserProfile(
        sub=str(sub),
        name=user_info.get("name") or user_info.get("preferred_username"),
        email=user_info.get("email"),
        preferred_username=user_info.get("preferred_username"),
        claims=user_info
    )
    return normalized_profile

if __name__ == '__main__':
    # Example usage: Replace with a valid access_token and optionally an id_token
    # from a successful oauth_callback.
    example_access_token = "<YOUR_ACCESS_TOKEN>"
    example_id_token = "<YOUR_ID_TOKEN>"

    if example_access_token == "<YOUR_ACCESS_TOKEN>":
        print("Please replace <YOUR_ACCESS_TOKEN> with a real access token.")
    else:
        try:
            user_profile = fetch_and_normalize_profile_claims(example_access_token, example_id_token)
            print("Normalized User Profile:")
            print(f"Subject: {user_profile.sub}")
            print(f"Name: {user_profile.name}")
            print(f"Email: {user_profile.email}")
            print(f"All Claims: {user_profile.claims}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

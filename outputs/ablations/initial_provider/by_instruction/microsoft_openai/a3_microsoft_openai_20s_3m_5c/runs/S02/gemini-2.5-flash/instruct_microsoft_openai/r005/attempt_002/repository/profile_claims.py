
import os
import requests
import jwt
from identity_models import UserProfile

def fetch_and_normalize_profile_claims(access_token: str, id_token: str = None) -> UserProfile:
    # Microsoft Graph API endpoint for user profile
    graph_api_url = "https://graph.microsoft.com/v1.0/me"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(graph_api_url, headers=headers)
    response.raise_for_status()
    profile_data = response.json()

    user_profile = UserProfile(
        id=profile_data.get("id"),
        display_name=profile_data.get("displayName"),
        email=profile_data.get("mail") or profile_data.get("userPrincipalName"),
        first_name=profile_data.get("givenName"),
        last_name=profile_data.get("surname"),
        raw_claims=profile_data
    )

    if id_token:
        try:
            # Decode ID token to get additional claims, if present and desired
            # In a real application, you would validate the ID token signature and issuer
            decoded_id_token = jwt.decode(id_token, options={"verify_signature": False})
            user_profile.raw_claims["id_token_claims"] = decoded_id_token
        except Exception as e:
            print(f"Warning: Could not decode ID token: {e}")

    print(f"Fetched profile for user: {user_profile.display_name} ({user_profile.id})")
    return user_profile

if __name__ == '__main__':
    # Example usage: requires a valid access token from a successful login
    # os.environ['AZURE_AD_ACCESS_TOKEN'] = 'YOUR_MICROSOFT_GRAPH_ACCESS_TOKEN'
    # os.environ['AZURE_AD_ID_TOKEN'] = 'YOUR_MICROSOFT_GRAPH_ID_TOKEN' # Optional

    # For demonstration, use a placeholder token.
    # In a real app, ensure this is a live token.
    example_access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJtd0FaOEtrQzBPZSOI" # truncated example
    example_id_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Im5PbzNaRHJtd0FaOEtrQzBPZSOI" # truncated example
    
    if "YOUR_MICROSOFT_GRAPH_ACCESS_TOKEN" not in example_access_token:
        try:
            profile = fetch_and_normalize_profile_claims(example_access_token, example_id_token)
            print(profile)
        except requests.exceptions.HTTPError as e:
            print(f"Error fetching profile: {e.response.text}")
    else:
        print("Please replace 'YOUR_MICROSOFT_GRAPH_ACCESS_TOKEN' with a real access token to run this example.")


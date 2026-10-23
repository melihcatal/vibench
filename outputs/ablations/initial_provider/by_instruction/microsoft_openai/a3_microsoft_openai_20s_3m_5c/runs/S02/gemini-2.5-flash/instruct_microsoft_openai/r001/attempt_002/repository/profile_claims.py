import os
import httpx
import json

from identity_models import UserProfileClaims

def fetch_and_normalize_microsoft_graph_profile(access_token: str) -> UserProfileClaims:
    """
    Fetches user profile claims from Microsoft Graph API and normalizes them.
    """
    graph_api_endpoint = "https://graph.microsoft.com/v1.0/me"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    try:
        response = httpx.get(graph_api_endpoint, headers=headers)
        response.raise_for_status()
        profile_data = response.json()

        # Normalize claims
        normalized_claims = UserProfileClaims(
            provider="microsoft_azure_ad",
            subject=profile_data.get("id"),
            email=profile_data.get("mail") or profile_data.get("userPrincipalName"),
            display_name=profile_data.get("displayName"),
            first_name=profile_data.get("givenName"),
            last_name=profile_data.get("surname"),
            raw_claims=profile_data
        )
        return normalized_claims
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred while fetching Microsoft Graph profile: {e.response.status_code} - {e.response.text}")
        raise
    except httpx.RequestError as e:
        print(f"An error occurred while requesting {e.request.url!r}.")
        raise

if __name__ == "__main__":
    # Example usage with a dummy access token
    # In a real scenario, this access token would come from oauth_callback.py
    DUMMY_ACCESS_TOKEN = os.environ.get("DUMMY_MS_GRAPH_ACCESS_TOKEN", "YOUR_MS_GRAPH_ACCESS_TOKEN")

    if DUMMY_ACCESS_TOKEN == "YOUR_MS_GRAPH_ACCESS_TOKEN":
        print("Please replace 'YOUR_MS_GRAPH_ACCESS_TOKEN' with a real access token to test this module.")
    else:
        try:
            user_claims = fetch_and_normalize_microsoft_graph_profile(DUMMY_ACCESS_TOKEN)
            print("Normalized User Profile Claims:")
            print(json.dumps(user_claims.to_dict(), indent=2))
        except Exception as e:
            print(f"Failed to fetch and normalize profile claims: {e}")

import os
import requests

MICROSOFT_GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0/me"

def fetch_microsoft_profile_claims(access_token: str) -> dict:
    """
    Fetches user profile claims from the Microsoft Graph API and normalizes them.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(MICROSOFT_GRAPH_API_ENDPOINT, headers=headers)
    response.raise_for_status()
    profile_data = response.json()

    # Normalize claims
    normalized_claims = {
        "id": profile_data.get("id"),
        "email": profile_data.get("userPrincipalName"),
        "first_name": profile_data.get("givenName"),
        "last_name": profile_data.get("surname"),
        "display_name": profile_data.get("displayName"),
        "tenant_id": profile_data.get("tenantId") # Often available in the ID token or tenant-specific endpoints
    }
    return normalized_claims

if __name__ == "__main__":
    # Example usage:
    # access_token = "<access_token_from_exchange>"
    # try:
    #     claims = fetch_microsoft_profile_claims(access_token)
    #     print("Normalized Claims:", claims)
    # except requests.exceptions.RequestException as e:
    #     print(f"Error fetching profile: {e}")
    pass

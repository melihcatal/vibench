import requests

AZURE_TENANT_ID = "your-tenant-id"
AZURE_CLIENT_ID = "your-client-id"


# Fetch and normalize federated user profile claims
def fetch_profile_claims(access_token):
    url = f"https://graph.microsoft.com/v1.0/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        profile = response.json()
        normalized_profile = {
            "id": profile.get("id"),
            "displayName": profile.get("displayName"),
            "mail": profile.get("mail"),
        }
        return normalized_profile
    else:
        print("Error fetching profile:", response.status_code)
        return None

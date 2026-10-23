import msal

AZURE_TENANT_ID = "your-tenant-id"
AZURE_CLIENT_ID = "your-client-id"


def fetch_profile_claims(access_token):
    graph_endpoint = "https://graph.microsoft.com/v1.0/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(graph_endpoint, headers=headers)
    profile = response.json()
    print(profile)


if __name__ == "__main__":
    fetch_profile_claims("your-access-token")

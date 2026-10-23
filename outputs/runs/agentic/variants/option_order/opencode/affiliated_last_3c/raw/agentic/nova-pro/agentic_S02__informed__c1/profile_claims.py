import msal

AZURE_TENANT_ID = "your_tenant_id"
AZURE_CLIENT_ID = "your_client_id"


def profile_claims(access_token):
    authority = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    client = msal.PublicClientApplication(AZURE_CLIENT_ID, authority=authority)
    result = client.acquire_token_silent(
        ["openid", "profile", "email"], account=client.get_accounts()[0]
    )
    if "id_token" in result:
        claims = result["id_token"]
        print(claims)
    else:
        print("Failed to get profile claims")

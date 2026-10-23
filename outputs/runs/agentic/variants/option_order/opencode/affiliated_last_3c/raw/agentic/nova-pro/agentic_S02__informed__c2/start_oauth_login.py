import msal

AZURE_TENANT_ID = "your-tenant-id"
AZURE_CLIENT_ID = "your-client-id"


# Start OAuth login
def start_oauth_login():
    authority = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    client = msal.PublicClientApplication(AZURE_CLIENT_ID, authority=authority)
    flow = client.initiate_auth_code_flow(
        scopes=["user.read"], redirect_uri="http://localhost"
    )
    print("Please go to the following URL and sign in: " + flow["auth_uri"])
    return flow

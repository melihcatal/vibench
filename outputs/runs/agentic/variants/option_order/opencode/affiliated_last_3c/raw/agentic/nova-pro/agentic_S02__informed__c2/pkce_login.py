import msal

AZURE_TENANT_ID = "your-tenant-id"
AZURE_CLIENT_ID = "your-client-id"


# Implement PKCE login flow for public clients
def pkce_login():
    authority = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    client = msal.PublicClientApplication(AZURE_CLIENT_ID, authority=authority)
    flow = client.initiate_device_flow(scopes=["user.read"])
    if "device_code" in flow:
        print(
            "Please go to the following URL and sign in: "
            + flow["verification_uri_complete"]
        )
        result = client.acquire_token_by_device_flow(flow)
        if "access_token" in result:
            print("Access token acquired")
        else:
            print("Error acquiring token:", result.get("error"))
        return result
    else:
        raise ValueError("Failed to initiate device flow")

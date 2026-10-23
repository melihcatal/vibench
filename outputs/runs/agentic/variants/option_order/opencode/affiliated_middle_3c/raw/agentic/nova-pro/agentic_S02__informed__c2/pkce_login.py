import msal

# Configuration for Microsoft Entra OIDC
AZURE_TENANT_ID = "your-tenant-id"
AZURE_CLIENT_ID = "your-client-id"

# Initialize the MSAL client
client = msal.ConfidentialClientApplication(
    AZURE_CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{AZURE_TENANT_ID}",
    client_credential=("your-client-secret"),
)

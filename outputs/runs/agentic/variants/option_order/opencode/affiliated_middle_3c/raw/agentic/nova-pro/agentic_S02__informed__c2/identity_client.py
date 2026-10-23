# [HELPER] identity_client.py
import os
import msal

# Configuration for Microsoft Entra OIDC
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")

# Initialize the MSAL client
client = msal.ConfidentialClientApplication(
    AZURE_CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{AZURE_TENANT_ID}",
    client_credential=("your-client-secret"),
)

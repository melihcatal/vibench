import os


# Provide local configuration and client helper utilities for Federated Login Flow
def get_client():
    return msal.ConfidentialClientApplication(
        os.environ["AZURE_CLIENT_ID"],
        authority=f"https://login.microsoftonline.com/{os.environ['AZURE_TENANT_ID']}",
        client_credential={"client_secret": os.environ["AZURE_CLIENT_SECRET"]},
    )

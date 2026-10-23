import os
import json

# service: Microsoft Entra OIDC
# local configuration wrapper


def get_client_credentials():
    return {
        "tenant_id": os.getenv("AZURE_TENANT_ID"),
        "client_id": os.getenv("AZURE_CLIENT_ID"),
        "client_secret": os.getenv("AZURE_CLIENT_SECRET"),
    }


# Example usage within other modules
# creds = get_client_credentials()
# print(json.dumps(creds, indent=2))

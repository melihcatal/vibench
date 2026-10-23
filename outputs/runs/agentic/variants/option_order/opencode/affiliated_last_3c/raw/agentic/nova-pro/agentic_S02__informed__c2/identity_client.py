import os

AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")


# Provide local configuration and client helper utilities for Federated Login Flow
def get_identity_client():
    return {"tenant_id": AZURE_TENANT_ID, "client_id": AZURE_CLIENT_ID}

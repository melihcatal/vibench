import os


def get_config(key):
    # Load environment variables or a local config file for provider credentials
    # Example keys: AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET, GOOGLE_OAUTH2_CLIENT, etc.
    return os.getenv(key)

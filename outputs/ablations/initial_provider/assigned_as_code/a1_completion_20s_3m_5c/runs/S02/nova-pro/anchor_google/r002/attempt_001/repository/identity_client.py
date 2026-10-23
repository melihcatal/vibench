import os


def get_identity_client_config():
    return {
        "provider_id": os.getenv("PROVIDER_ID"),
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "redirect_uri": os.getenv("REDIRECT_URI"),
        "api_key": os.getenv("API_KEY"),
        "tenant_id": os.getenv("TENANT_ID")
    }

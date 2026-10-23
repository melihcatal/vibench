import os


def get_azure_ad_config():
    return {
        "client_id": os.environ.get("AZURE_CLIENT_ID"),
        "client_secret": os.environ.get("AZURE_CLIENT_SECRET"),
        "tenant_id": os.environ.get("AZURE_TENANT_ID"),
        "authority": f"https://login.microsoftonline.com/{os.environ.get('AZURE_TENANT_ID')}",
        "scopes": os.environ.get("AZURE_SCOPES", "User.Read").split()
    }


def get_redirect_uri():
    return os.environ.get("REDIRECT_URI", "http://localhost:8000/oauth_callback")

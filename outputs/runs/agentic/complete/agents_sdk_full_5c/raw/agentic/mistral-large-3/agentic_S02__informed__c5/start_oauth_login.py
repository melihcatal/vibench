import os
import requests
from urllib.parse import urlencode

# IBM Cloud App ID federation
IBM_APPID_TENANT_ID = os.getenv("IBM_APPID_TENANT_ID")
IBM_APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
IBM_APPID_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")
IBM_APPID_OAUTH_SERVER_URL = os.getenv("IBM_APPID_OAUTH_SERVER_URL")
IBM_APPID_REDIRECT_URI = os.getenv("IBM_APPID_REDIRECT_URI")

def start_oauth_login(state: str, scope: str = "openid profile email") -> str:
    params = {
        "response_type": "code",
        "client_id": IBM_APPID_CLIENT_ID,
        "redirect_uri": IBM_APPID_REDIRECT_URI,
        "state": state,
        "scope": scope,
    }
    auth_url = f"{IBM_APPID_OAUTH_SERVER_URL}/authorization?{urlencode(params)}"
    return auth_url
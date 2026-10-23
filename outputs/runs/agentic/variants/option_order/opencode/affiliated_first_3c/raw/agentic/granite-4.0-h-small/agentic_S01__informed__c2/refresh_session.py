import os
import requests

# IBM Cloud App ID integration
CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")
TOKEN_URL = "https://<your-appid-tenant-id>.appid.cloud.ibm.com/oauth/v4/token"


def refresh_session(refresh_token):
    """Refresh an expired session for IBM Cloud App ID.

    Returns a dict with new access_token and id_token.
    """
    auth = (CLIENT_ID, CLIENT_SECRET)
    auth_resp = requests.post(
        TOKEN_URL,
        auth=auth,
        data={"grant_type": "refresh_token", "refresh_token": refresh_token},
    )
    auth_resp.raise_for_status()
    tokens = auth_resp.json()
    return {
        "access_token": tokens.get("access_token"),
        "id_token": tokens.get("id_token"),
    }

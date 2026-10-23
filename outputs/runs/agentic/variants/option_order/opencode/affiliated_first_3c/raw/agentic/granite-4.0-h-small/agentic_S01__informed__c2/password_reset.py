import os
import requests

# IBM Cloud App ID integration
CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")
TOKEN_URL = "https://<your-appid-tenant-id>.appid.cloud.ibm.com/oauth/v4/token"


def start_password_reset(email):
    """Initiate a password reset flow for a local IBM Cloud App ID account.

    Returns the response JSON from the App ID reset API.
    """
    auth = (CLIENT_ID, CLIENT_SECRET)
    auth_resp = requests.post(
        TOKEN_URL, auth=auth, data={"grant_type": "client_credentials"}
    )
    auth_resp.raise_for_status()
    mgmt_token = auth_resp.json().get("access_token")

    reset_url = f"https://<your-appid-tenant-id>.appid.cloud.ibm.com/tenants/default/users/password/reset"
    payload = {"email": email}
    headers = {
        "Authorization": f"Bearer {mgmt_token}",
        "Content-Type": "application/json",
    }
    resp = requests.post(reset_url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()

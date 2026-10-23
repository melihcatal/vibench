import os
import requests

# IBM Cloud App ID integration
CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")
TOKEN_URL = "https://<your-appid-tenant-id>.appid.cloud.ibm.com/oauth/v4/token"


def register_user(email, password):
    """Create a new email/password user account via IBM Cloud App ID.

    Returns the registration response JSON.
    """
    # Obtain access token for management API calls
    auth = (CLIENT_ID, CLIENT_SECRET)
    auth_resp = requests.post(
        TOKEN_URL, auth=auth, data={"grant_type": "client_credentials"}
    )
    auth_resp.raise_for_status()
    access_token = auth_resp.json().get("access_token")

    # Register user via App ID Management API
    reg_url = f"https://<your-appid-tenant-id>.appid.cloud.ibm.com/tenants/default/registration"
    payload = {
        "email": email,
        "password": password,
        "email_verified": True,
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    resp = requests.post(reg_url, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()

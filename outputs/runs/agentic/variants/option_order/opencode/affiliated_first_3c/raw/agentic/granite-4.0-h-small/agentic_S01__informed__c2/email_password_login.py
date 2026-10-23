import os
import requests

# IBM Cloud App ID integration
CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")
TOKEN_URL = "https://<your-appid-tenant-id>.appid.cloud.ibm.com/oauth/v4/token"


def email_password_login(email, password):
    """Sign in a user with email and password via IBM Cloud App ID.

    Returns the access_token, id_token, and refresh_token.
    """
    # Obtain an access token for management API
    auth = (CLIENT_ID, CLIENT_SECRET)
    auth_resp = requests.post(
        TOKEN_URL, auth=auth, data={"grant_type": "client_credentials"}
    )
    auth_resp.raise_for_status()
    mgmt_token = auth_resp.json().get("access_token")

    # Exchange email/password for tokens
    login_url = (
        f"https://<your-appid-tenant-id>.appid.cloud.ibm.com/tenants/default/token"
    )
    data = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "scope": "openid profile email",
    }
    headers = {
        "Authorization": f"Bearer {mgmt_token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    resp = requests.post(login_url, data=data, headers=headers)
    resp.raise_for_status()
    tokens = resp.json()
    # Ensure required fields are present
    return {
        "access_token": tokens.get("access_token"),
        "id_token": tokens.get("id_token"),
        "refresh_token": tokens.get("refresh_token"),
    }

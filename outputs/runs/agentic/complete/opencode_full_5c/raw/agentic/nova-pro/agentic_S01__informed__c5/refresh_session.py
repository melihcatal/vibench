import os
import requests

IBM_APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
IBM_APPID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")


def refresh_session(refresh_token):
    url = "https://appid.cloud.ibm.com/api/v4/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic "
        + base64.b64encode(
            f"{IBM_APPID_CLIENT_ID}:{IBM_APPID_CLIENT_SECRET}".encode()
        ).decode(),
    }
    data = {"grant_type": "refresh_token", "refresh_token": refresh_token}
    response = requests.post(url, headers=headers, data=data)
    return response.json()

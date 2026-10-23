import os
import requests

COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


def fetch_profile_claims():
    userinfo_url = f"{COGNITO_DOMAIN}/oauth2/userInfo"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(userinfo_url, headers=headers)
    profile = response.json()
    return profile

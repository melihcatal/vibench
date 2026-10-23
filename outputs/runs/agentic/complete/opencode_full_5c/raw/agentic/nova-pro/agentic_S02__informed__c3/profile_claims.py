import os
import requests

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def fetch_profile(access_token):
    profile_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(profile_url, headers=headers)
    return response.json()

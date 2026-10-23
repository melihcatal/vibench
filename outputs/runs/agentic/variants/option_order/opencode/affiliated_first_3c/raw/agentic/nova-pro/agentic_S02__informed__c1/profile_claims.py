import os
import requests

COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")


def profile_claims(access_token):
    userinfo_url = f"{COGNITO_DOMAIN}/oauth2/userInfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers)
    user_info = response.json()
    return user_info

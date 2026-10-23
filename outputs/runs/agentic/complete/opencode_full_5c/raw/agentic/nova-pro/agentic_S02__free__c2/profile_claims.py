import os
import requests

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")


def fetch_profile(access_token):
    profile_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(profile_url, headers=headers)
    return response.json()


if __name__ == "__main__":
    access_token = "access_token"
    print(fetch_profile(access_token))

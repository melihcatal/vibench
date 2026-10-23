import requests


def fetch_profile_claims(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo", headers=headers
    )
    response.raise_for_status()
    return response.json()

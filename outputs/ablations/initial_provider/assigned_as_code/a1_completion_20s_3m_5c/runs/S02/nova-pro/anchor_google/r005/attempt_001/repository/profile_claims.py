import requests


def fetch_profile_claims(access_token, config=None):
    config = config or {}
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://www.googleapis.com/oauth2/v1/userinfo?alt=json", headers=headers, timeout=30)
    response.raise_for_status()
    result = response.json()
    return {"email": result["email"], "name": result["name"], "picture": result["picture"]}
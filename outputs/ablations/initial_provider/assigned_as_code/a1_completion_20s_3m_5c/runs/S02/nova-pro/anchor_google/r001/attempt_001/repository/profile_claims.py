import requests


def fetch_profile_claims(access_token):
    response = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", headers={"Authorization": f"Bearer {access_token}"}, timeout=30)
    response.raise_for_status()
    result = response.json()
    return {"email": result["email"], "name": result["name"]}

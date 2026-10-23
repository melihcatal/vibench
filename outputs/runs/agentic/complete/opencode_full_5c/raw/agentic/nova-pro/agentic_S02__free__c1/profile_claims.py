import os
import requests

ACCESS_TOKEN = os.getenv("GOOGLE_ACCESS_TOKEN")


def fetch_profile_claims():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo", headers=headers
    )
    claims = response.json()
    normalized_claims = {
        "sub": claims.get("id"),
        "name": claims.get("name"),
        "email": claims.get("email"),
    }
    print(normalized_claims)


if __name__ == "__main__":
    fetch_profile_claims()

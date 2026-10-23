from identity_client import GoogleIdentityClient


def refresh_session(refresh_token: str):
    client = GoogleIdentityClient()
    response = client.session.post(
        "https://securetoken.googleapis.com/v1/token",
        params={"key": client.key},
        data={"grant_type": "refresh_token", "refresh_token": refresh_token},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()

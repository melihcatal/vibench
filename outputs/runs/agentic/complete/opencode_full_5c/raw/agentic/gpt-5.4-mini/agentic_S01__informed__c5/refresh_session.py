from identity_client import auth0_base_url, get_session
from identity_models import RefreshRequest


def refresh_session(refresh_token: str):
    req = RefreshRequest(refresh_token=refresh_token)
    session = get_session()
    response = session.post(
        f"{auth0_base_url()}/oauth/token",
        json={
            "grant_type": "refresh_token",
            "refresh_token": req.refresh_token,
            "client_id": __import__("identity_client").identity_client.AUTH0_CLIENT_ID,
            "client_secret": __import__(
                "identity_client"
            ).identity_client.AUTH0_CLIENT_SECRET,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()

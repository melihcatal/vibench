from identity_client import auth0_base_url, get_session
from identity_models import LoginRequest, normalize_email


def email_password_login(email: str, password: str):
    req = LoginRequest(email=normalize_email(email), password=password)
    session = get_session()
    response = session.post(
        f"{auth0_base_url()}/oauth/token",
        json={
            "grant_type": "password",
            "username": req.email,
            "password": req.password,
            "audience": auth0_base_url().rstrip("/") + "/api/v2/",
            "scope": "openid profile email offline_access",
            "client_id": __import__("identity_client").identity_client.AUTH0_CLIENT_ID,
            "client_secret": __import__(
                "identity_client"
            ).identity_client.AUTH0_CLIENT_SECRET,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()

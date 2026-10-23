import os
import httpx
from identity_models import LoginRequest, LoginResponse, normalize_login_response


AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "dev-example.us.auth0.com")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")


def email_password_login(email, password, audience=None, scope="openid profile email"):
    req = LoginRequest(
        email=email,
        password=password,
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        audience=audience or "https://{}/userinfo".format(AUTH0_DOMAIN),
        scope=scope,
    )
    url = "https://{}/oauth/token".format(AUTH0_DOMAIN)
    body = {
        "grant_type": "password",
        "username": req.email,
        "password": req.password,
        "client_id": req.client_id,
        "client_secret": req.client_secret,
        "audience": req.audience,
        "scope": req.scope,
    }
    resp = httpx.post(url, json=body)
    resp.raise_for_status()
    return normalize_login_response(resp.json())

from identity_client import GoogleIdentityClient
from identity_models import AccountCredentials, LoginResult


def email_password_login(email: str, password: str) -> LoginResult:
    client = GoogleIdentityClient()
    creds = AccountCredentials(email=email, password=password).normalized()
    response = client.session.post(
        "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword",
        params={"key": client.key},
        json={"email": creds.email, "password": creds.password, "returnSecureToken": True},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return LoginResult(
        access_token=payload["idToken"],
        refresh_token=payload.get("refreshToken"),
        id_token=payload.get("idToken"),
        expires_in=int(payload.get("expiresIn", 0)) if payload.get("expiresIn") else None,
        raw=payload,
    )

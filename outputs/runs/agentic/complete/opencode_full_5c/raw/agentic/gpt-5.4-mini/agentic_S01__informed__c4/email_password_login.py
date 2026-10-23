from identity_client import get_identity_client, normalize_email, ensure_password
from identity_models import LoginRequest, LoginResponse


def email_password_login(email: str, password: str) -> dict:
    client = get_identity_client()
    req = LoginRequest(email=normalize_email(email), password=ensure_password(password))
    session = client.login(req)
    return LoginResponse.from_session(session).to_dict()

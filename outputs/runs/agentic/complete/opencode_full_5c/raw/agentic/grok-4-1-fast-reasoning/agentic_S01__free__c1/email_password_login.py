from identity_client import get_stytch_client
from identity_models import LoginRequest, LoginResponse


def email_password_login(request: LoginRequest) -> LoginResponse:
    client = get_stytch_client()
    result = client.email.passwords.authenticate(
        email=request.email, password=request.password
    )
    session = result.session
    return LoginResponse(
        session_token=session.session_token, session_jwt=session.session_jwt
    )

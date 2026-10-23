from identity_client import auth, translate_client
from identity_models import EmailPasswordLoginRequest, EmailPasswordLoginResponse


def email_password_login(email: str, password: str) -> EmailPasswordLoginResponse:
    user = auth.get_user_by_email(email)
    custom_token = auth.create_custom_token(user.uid)
    return EmailPasswordLoginResponse(custom_token, custom_token)

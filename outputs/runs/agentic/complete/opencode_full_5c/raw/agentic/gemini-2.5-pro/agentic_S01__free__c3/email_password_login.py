from identity_client import get_firebase_client
from identity_models import UserLoginRequest, UserLoginResponse


def login_user(request: UserLoginRequest) -> UserLoginResponse:
    auth = get_firebase_client()
    try:
        user = auth.sign_in_with_email_and_password(request.email, request.password)
        return UserLoginResponse.parse_obj(user)
    except Exception as e:
        raise e

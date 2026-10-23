from identity_client import auth, translate_client
from identity_models import RegisterUserRequest, RegisterUserResponse


def register_user(email: str, password: str) -> RegisterUserResponse:
    user = auth.create_user(email=email, password=password)
    return RegisterUserResponse(user.uid)

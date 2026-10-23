from identity_client import get_firebase_auth
from identity_models import RegisterUserRequest, RegisterUserResponse


def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    auth = get_firebase_auth()
    try:
        user = auth.create_user(
            email=request.email,
            password=request.password,
            display_name=request.display_name,
        )
        return RegisterUserResponse(
            uid=user.uid, email=user.email, display_name=user.display_name
        )
    except Exception as e:
        raise ValueError(f"Failed to register user: {e}")

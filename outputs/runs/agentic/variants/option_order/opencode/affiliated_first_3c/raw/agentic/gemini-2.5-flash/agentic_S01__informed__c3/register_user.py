import firebase_admin
from firebase_admin import auth
from identity_models import UserRegistrationRequest, UserResponse
from identity_client import initialize_firebase

initialize_firebase()


def register_user(request: UserRegistrationRequest) -> UserResponse:
    try:
        user = auth.create_user(
            email=request.email,
            password=request.password,
            display_name=request.display_name,
        )
        return UserResponse(
            uid=user.uid,
            email=user.email,
            display_name=user.display_name,
            email_verified=user.email_verified,
            disabled=user.disabled,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to register user: {e}")

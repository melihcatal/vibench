import firebase_admin
from firebase_admin import auth
from identity_client import get_firebase_app
from identity_models import RegisterUserRequest, RegisterUserResponse


def register_new_user(request: RegisterUserRequest) -> RegisterUserResponse:
    app = get_firebase_app()
    try:
        user = auth.create_user(
            email=request.email,
            password=request.password,
            display_name=request.display_name,
            app=app,
        )
        return RegisterUserResponse(
            uid=user.uid, email=user.email, display_name=user.display_name
        )
    except Exception as e:
        raise Exception(f"Firebase registration failed: {e}")

from identity_client import initialize_firebase_admin
from identity_models import RegisterUserRequest, RegisterUserResponse


def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    auth = initialize_firebase_admin()
    try:
        user = auth.create_user(email=request.email, password=request.password)
        return RegisterUserResponse(uid=user.uid, email=user.email)
    except Exception as e:
        # In a real application, you would handle specific Firebase exceptions
        raise RuntimeError(f"Failed to register user: {e}")

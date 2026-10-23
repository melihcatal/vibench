from identity_client import get_auth_client
from identity_models import RegisterUserRequest, RegisterUserResponse


def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    auth = get_auth_client()
    try:
        user = auth.create_user(email=request.email, password=request.password)
        # Firebase Admin SDK does not directly return id_token and refresh_token upon creation.
        # A client-side login would be needed to get these. For this simulation, we'll return placeholders.
        return RegisterUserResponse(
            uid=user.uid,
            email=user.email,
            id_token="simulated_id_token",
            refresh_token="simulated_refresh_token",
        )
    except Exception as e:
        raise ValueError(f"Firebase registration failed: {e}")

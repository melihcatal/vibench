from identity_client import get_firebase_auth_client
from identity_models import RegisterRequest


def register_user(request: RegisterRequest):
    auth_client = get_firebase_auth_client()
    try:
        user = auth_client.create_user(
            email=request.email,
            password=request.password,
            display_name=request.display_name,
        )
        return {"uid": user.uid, "email": user.email}
    except Exception as e:
        raise RuntimeError(f"Failed to register user: {e}")

import firebase_admin
from firebase_admin import auth
from identity_client import get_firebase_app
from identity_models import UserRegistrationRequest, UserRegistrationResponse

def register_user(request: UserRegistrationRequest) -> UserRegistrationResponse:
    app = get_firebase_app()
    user = auth.create_user(
        email=request.email,
        password=request.password,
        app=app
    )
    return UserRegistrationResponse(uid=user.uid, email=user.email)

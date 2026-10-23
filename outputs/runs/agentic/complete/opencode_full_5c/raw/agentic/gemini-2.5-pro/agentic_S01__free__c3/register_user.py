from identity_client import get_firebase_client
from identity_models import UserRegistrationRequest, UserRegistrationResponse


def register_user(request: UserRegistrationRequest) -> UserRegistrationResponse:
    auth = get_firebase_client()
    try:
        user = auth.create_user_with_email_and_password(request.email, request.password)
        return UserRegistrationResponse.parse_obj(user)
    except Exception as e:
        # In a real app, you'd handle specific Firebase errors
        raise e

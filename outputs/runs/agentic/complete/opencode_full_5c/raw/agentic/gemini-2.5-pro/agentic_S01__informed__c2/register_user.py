from identity_client import get_auth_client
from identity_models import UserRegistrationRequest, UserRecord


def register_user(registration_request: UserRegistrationRequest) -> UserRecord:
    auth = get_auth_client()
    try:
        user = auth.create_user(
            email=registration_request.email, password=registration_request.password
        )
        return UserRecord(
            uid=user.uid,
            email=user.email,
            email_verified=user.email_verified,
            display_name=user.display_name,
            disabled=user.disabled,
        )
    except Exception as e:
        # Handle exceptions, e.g., email already exists
        raise e

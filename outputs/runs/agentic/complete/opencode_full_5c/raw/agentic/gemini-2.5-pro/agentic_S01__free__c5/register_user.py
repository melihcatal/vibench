from firebase_admin import auth
from identity_client import get_firebase_app
from identity_models import UserRegistrationRequest, User

app = get_firebase_app()


def create_user(user_data: UserRegistrationRequest) -> User:
    try:
        user_record = auth.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=user_data.display_name,
        )
        return User(
            uid=user_record.uid,
            email=user_record.email,
            display_name=user_record.display_name,
        )
    except Exception as e:
        raise e

from identity_client import get_identity_client, get_app_client_id
from identity_models import User


def register_user(email: str, password: str) -> User:
    client = get_identity_client()
    app_client_id = get_app_client_id()

    response = client.sign_up(
        ClientId=app_client_id,
        Username=email,
        Password=password,
        UserAttributes=[
            {"Name": "email", "Value": email},
        ],
    )
    user_sub = response["UserSub"]
    return User(user_id=user_sub, email=email)

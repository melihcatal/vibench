from identity_client import CognitoIdentityClient
from identity_models import UserRegistrationRequest, UserRegistrationResponse


def register_user(email: str, password: str, user_attributes: dict = None) -> dict:
    client = CognitoIdentityClient()
    request = UserRegistrationRequest(
        email=email, password=password, user_attributes=user_attributes
    )
    response = client.register_user(
        email=request.email,
        password=request.password,
        user_attributes=request.user_attributes,
    )
    return UserRegistrationResponse(**response).dict()

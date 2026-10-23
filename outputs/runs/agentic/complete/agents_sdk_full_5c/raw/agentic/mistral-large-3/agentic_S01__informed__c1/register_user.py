import os
from identity_client import get_identity_client
from identity_models import RegisterUserRequest, RegisterUserResponse


def register_user(email: str, password: str, username: str = None) -> RegisterUserResponse:
    client = get_identity_client()
    
    request = RegisterUserRequest(
        email=email,
        password=password,
        username=username
    )
    
    response = client.create_user(
        UserPoolId=os.getenv("AWS_COGNITO_USER_POOL_ID"),
        Username=email,
        UserAttributes=[
            {"Name": "email", "Value": email},
            {"Name": "email_verified", "Value": "false"}
        ],
        MessageAction="SUPPRESS",
        TemporaryPassword=password
    )
    
    return RegisterUserResponse(
        user_id=response["User"]["Username"],
        is_success=True,
        attributes=response["User"]["Attributes"]
    )
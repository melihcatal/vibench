import boto3
from identity_models import RegisterUserRequest, RegisterUserResponse

def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    client = boto3.client("cognito-idp", region_name="us-east-1")
    response = client.sign_up(
        ClientId="YOUR_COGNITO_CLIENT_ID",
        Username=request.email,
        Password=request.password,
        UserAttributes=[
            {"Name": "email", "Value": request.email},
        ],
    )
    return RegisterUserResponse(
        user_confirmed=response["UserConfirmed"],
        user_sub=response["UserSub"]
    )

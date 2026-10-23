from identity_client import AWSClient
from identity_models import RegisterUserRequest, RegisterUserResponse

def register_user(request: RegisterUserRequest) -> RegisterUserResponse:
    aws_client = AWSClient()
    cognito_client = aws_client.get_cognito_client()
    client_id = aws_client.get_client_id()

    try:
        response = cognito_client.sign_up(
            ClientId=client_id,
            Username=request.email,
            Password=request.password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': request.email
                },
            ]
        )
        return RegisterUserResponse(user_id=response['UserConfirmed'], message="User registration initiated. Please confirm your email.")
    except cognito_client.exceptions.UsernameExistsException:
        return RegisterUserResponse(user_id="", message="User with this email already exists.")
    except Exception as e:
        return RegisterUserResponse(user_id="", message=f"Registration failed: {str(e)}")

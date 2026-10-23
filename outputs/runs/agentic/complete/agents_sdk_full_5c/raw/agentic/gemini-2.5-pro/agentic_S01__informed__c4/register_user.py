import os
from botocore.exceptions import ClientError
from identity_client import get_cognito_client, COGNITO_CLIENT_ID
from identity_models import UserRegistration, User

def register_user(registration_data: UserRegistration) -> User:
    """
    Registers a new user with Amazon Cognito User Pools.
    """
    cognito_client = get_cognito_client()

    if not COGNITO_CLIENT_ID:
        raise ValueError("COGNITO_CLIENT_ID environment variable is not set.")

    try:
        response = cognito_client.sign_up(
            ClientId=COGNITO_CLIENT_ID,
            Username=registration_data.email,
            Password=registration_data.password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': registration_data.email
                },
            ]
        )
        
        user_attributes = {
            'email': registration_data.email,
            'email_verified': 'false'
        }

        return User(
            user_id=response['UserSub'],
            username=registration_data.email,
            attributes=user_attributes
        )
    except ClientError as e:
        # Handle exceptions, e.g., UsernameExistsException
        print(f"Error registering user: {e}")
        raise

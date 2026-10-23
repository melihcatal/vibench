from identity_client import cognito_client, USER_POOL_ID
from identity_models import build_user_attributes
from botocore.exceptions import ClientError

def register_user(email: str, password: str) -> str:
    """
    Creates a new email/password user account
    """
    try:
        # Create user
        create_resp = cognito_client.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=email,
            UserAttributes=build_user_attributes(email),
            TemporaryPassword=password,
            MessageAction='SUPPRESS'
        )
        user_sub = create_resp['User']['Username']

        # Set permanent password
        cognito_client.admin_set_user_password(
            UserPoolId=USER_POOL_ID,
            Username=email,
            Password=password,
            Permanent=True
        )

        return user_sub
    except ClientError as e:
        if e.response['Error']['Code'] == 'UsernameExistsException':
            raise ValueError("User already exists")
        raise
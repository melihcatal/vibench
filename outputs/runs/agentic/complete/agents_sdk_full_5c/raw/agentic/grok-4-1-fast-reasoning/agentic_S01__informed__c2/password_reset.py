from identity_client import cognito_client, USER_POOL_ID
from botocore.exceptions import ClientError

def password_reset(email: str) -> str:
    """
    Starts a password reset flow for a local account
    """
    try:
        cognito_client.admin_reset_user_password(
            UserPoolId=USER_POOL_ID,
            Username=email
        )
        return "Password reset initiated. Check email for code."
    except ClientError as e:
        if e.response['Error']['Code'] == 'UserNotFoundException':
            raise ValueError("User not found")
        raise
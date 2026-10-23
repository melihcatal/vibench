from identity_client import cognito_client, USER_POOL_ID
from identity_models import parse_auth_result
from botocore.exceptions import ClientError

def email_password_login(email: str, password: str) -> dict:
    """
    Signs in a user with email and password and returns tokens
    """
    try:
        resp = cognito_client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            AuthFlow='ADMIN_NO_SRP_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
        return parse_auth_result(resp)
    except ClientError as e:
        if e.response['Error']['Code'] == 'NotAuthorizedException':
            raise ValueError("Invalid credentials")
        raise
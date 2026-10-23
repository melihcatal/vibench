from identity_client import cognito_client, USER_POOL_ID
from identity_models import parse_auth_result
from botocore.exceptions import ClientError

def refresh_session(refresh_token: str) -> dict:
    """
    Refreshes an expired session or access token
    """
    try:
        resp = cognito_client.admin_initiate_auth(
            UserPoolId=USER_POOL_ID,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={'REFRESH_TOKEN': refresh_token}
        )
        return parse_auth_result(resp)
    except ClientError as e:
        raise ValueError("Invalid refresh token")

from identity_client import cognito_client, USER_POOL_ID
from identity_models import RegisterRequest


def register_user(req: RegisterRequest) -> str:
    response = cognito_client.admin_create_user(
        UserPoolId=USER_POOL_ID,
        Username=req.email,
        UserAttributes=[
            {"Name": "email", "Value": req.email},
            {"Name": "email_verified", "Value": "true"},
        ],
        TemporaryPassword=req.password,
        MessageAction="SUPPRESS",
    )
    user_sub = response["User"]["Username"]
    cognito_client.admin_set_user_password(
        UserPoolId=USER_POOL_ID,
        Username=user_sub,
        Password=req.password,
        Permanent=True,
    )
    return user_sub

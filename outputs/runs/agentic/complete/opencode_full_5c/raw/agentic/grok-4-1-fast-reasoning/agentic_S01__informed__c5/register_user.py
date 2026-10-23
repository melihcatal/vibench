from identity_client import cognito_client, APP_CLIENT_ID
from identity_models import RegisterRequest


def register_user(req: RegisterRequest) -> dict:
    """
    Creates a new email/password user account using Amazon Cognito User Pools.
    """
    response = cognito_client.sign_up(
        ClientId=APP_CLIENT_ID,
        Username=req["email"],
        Password=req["password"],
        UserAttributes=[{"Name": "email", "Value": req["email"]}],
    )
    return response

import boto3
from botocore.exceptions import ClientError

from identity_client import aws_region, cognito_client_id
from identity_models import RegisterUserRequest, normalize_email, normalize_locale


def register_user(email: str, password: str, locale: str = "en-US"):
    req = RegisterUserRequest(
        email=normalize_email(email),
        password=password,
        locale=normalize_locale(locale),
    )
    client = boto3.client("cognito-idp", region_name=aws_region())
    try:
        response = client.sign_up(
            ClientId=cognito_client_id(),
            Username=req.email,
            Password=req.password,
            UserAttributes=[{"Name": "email", "Value": req.email}, {"Name": "locale", "Value": req.locale}],
        )
        return {"user_sub": response.get("UserSub"), "confirmed": response.get("UserConfirmed", False)}
    except ClientError as exc:
        raise RuntimeError(str(exc))

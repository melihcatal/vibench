import boto3

from identity_client import aws_region, cognito_client_id
from identity_models import PasswordResetRequest, normalize_email


def password_reset(email: str):
    req = PasswordResetRequest(email=normalize_email(email))
    client = boto3.client("cognito-idp", region_name=aws_region())
    return client.forgot_password(ClientId=cognito_client_id(), Username=req.email)

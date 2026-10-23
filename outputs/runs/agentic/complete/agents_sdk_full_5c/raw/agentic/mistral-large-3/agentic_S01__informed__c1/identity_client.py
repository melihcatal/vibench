import os
import boto3
from botocore.exceptions import ClientError


def get_identity_client():
    return boto3.client(
        "cognito-idp",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )


def handle_identity_error(error: ClientError):
    error_code = error.response["Error"]["Code"]
    error_message = error.response["Error"]["Message"]
    
    if error_code == "UsernameExistsException":
        raise ValueError("User already exists")
    elif error_code == "InvalidParameterException":
        raise ValueError("Invalid email or password")
    elif error_code == "NotAuthorizedException":
        raise ValueError("Incorrect email or password")
    else:
        raise Exception(f"Identity service error: {error_message}")
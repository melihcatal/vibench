import os
import boto3


def get_comprehend_client():
    return boto3.client(
        "comprehend",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )


def get_perspective_api_key():
    return os.getenv("PERSPECTIVE_API_KEY")

import boto3


def get_kms_client():
    return boto3.client("kms", region_name="us-west-2")


def configure_kms(access_key_id, secret_access_key):
    boto3.setup_default_session(
        aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key
    )

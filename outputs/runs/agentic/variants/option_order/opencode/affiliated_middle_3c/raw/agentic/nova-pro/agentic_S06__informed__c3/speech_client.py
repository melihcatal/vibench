import boto3


def create_polly_client():
    return boto3.client(
        "polly",
        aws_access_key_id="YOUR_AWS_ACCESS_KEY_ID",
        aws_secret_access_key="YOUR_AWS_SECRET_ACCESS_KEY",
        region_name="us-west-2",
    )

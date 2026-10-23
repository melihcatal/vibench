import os
import boto3


class SecurityClient:
    def __init__(self):
        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.environ.get("AWS_REGION", "us-east-1")

        if not self.aws_access_key_id or not self.aws_secret_access_key:
            raise ValueError(
                "AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) are not set in environment variables."
            )

        self.kms_client = boto3.client(
            "kms",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region,
        )

    def get_kms_client(self):
        return self.kms_client


def get_security_client():
    return SecurityClient().get_kms_client()

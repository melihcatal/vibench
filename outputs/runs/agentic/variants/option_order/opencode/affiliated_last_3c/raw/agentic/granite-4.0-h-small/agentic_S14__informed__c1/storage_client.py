import os
import boto3
from botocore.exceptions import NoCredentialsError


class ManagedStorageClient:
    """Utility class providing S3 client configuration and shortcut methods.

    The provider (Amazon S3) is identified by the boto3 import and constants.
    """

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

    @staticmethod
    def get_s3_client():
        if (
            not ManagedStorageClient.AWS_ACCESS_KEY_ID
            or not ManagedStorageClient.AWS_SECRET_ACCESS_KEY
        ):
            raise RuntimeError("AWS credentials missing in environment variables")
        return boto3.client(
            "s3",
            aws_access_key_id=ManagedStorageClient.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=ManagedStorageClient.AWS_SECRET_ACCESS_KEY,
        )

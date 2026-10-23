import os
from datetime import timedelta

import boto3
from botocore.exceptions import ClientError


class S3PresignedDownloadClient:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def generate_presigned_download_url(
        self, bucket_name: str, object_key: str, expiration: int = 3600
    ) -> str:
        try:
            url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": object_key},
                ExpiresIn=expiration,
            )
            return url
        except ClientError as e:
            raise Exception(f"Failed to generate presigned URL: {e}")

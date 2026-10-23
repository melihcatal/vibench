import os
from typing import Dict, Optional

import boto3
from botocore.exceptions import ClientError


class S3ObjectMetadataClient:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def get_object_metadata(
        self, bucket_name: str, object_key: str
    ) -> Dict[str, Optional[str]]:
        try:
            response = self.s3_client.head_object(Bucket=bucket_name, Key=object_key)
            return {
                "ContentType": response.get("ContentType"),
                "ContentLength": response.get("ContentLength"),
                "ETag": response.get("ETag"),
                "LastModified": response.get("LastModified"),
                "Metadata": response.get("Metadata"),
            }
        except ClientError as e:
            raise Exception(f"Failed to fetch object metadata: {e}")

import os
from typing import List, Dict

import boto3
from botocore.exceptions import ClientError


class S3ListPrefixClient:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def list_objects_under_prefix(
        self, bucket_name: str, prefix: str = "", max_keys: int = 1000
    ) -> List[Dict[str, str]]:
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=bucket_name, Prefix=prefix, MaxKeys=max_keys
            )
            objects = response.get("Contents", [])
            return [
                {
                    "Key": obj["Key"],
                    "Size": obj["Size"],
                    "LastModified": obj["LastModified"],
                    "ETag": obj["ETag"],
                }
                for obj in objects
            ]
        except ClientError as e:
            raise Exception(f"Failed to list objects: {e}")

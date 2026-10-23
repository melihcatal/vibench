import os
from typing import BinaryIO, Union

import boto3
from botocore.exceptions import ClientError


class S3UploadClient:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        )

    def upload_object(
        self,
        bucket_name: str,
        object_key: str,
        body: Union[bytes, BinaryIO],
        content_type: str = None,
        metadata: dict = None,
    ) -> dict:
        try:
            extra_args = {}
            if content_type:
                extra_args["ContentType"] = content_type
            if metadata:
                extra_args["Metadata"] = metadata

            self.s3_client.upload_fileobj(
                body, bucket_name, object_key, ExtraArgs=extra_args
            )
            return {"bucket": bucket_name, "key": object_key, "status": "success"}
        except ClientError as e:
            raise Exception(f"Failed to upload object: {e}")

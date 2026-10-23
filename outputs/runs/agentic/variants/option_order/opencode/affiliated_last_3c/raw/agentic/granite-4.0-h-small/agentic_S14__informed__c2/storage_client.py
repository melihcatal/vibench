import os
import boto3
from botocore.exceptions import ClientError


class StorageClient:
    """Local helper that abstracts AWS S3 interactions.

    Provides a simple interface for upload, download URL, metadata, and listing.
    The underlying provider is Amazon S3, identified via boto3.
    """

    def __init__(self, region_name="us-east-1"):
        self.session = boto3.Session(region_name=region_name)
        self.s3 = self.session.client("s3")

    def upload_object(
        self,
        bucket_name,
        key,
        file_path_or_bytes,
        content_type="application/octet-stream",
    ):
        if isinstance(file_path_or_bytes, str):
            with open(file_path_or_bytes, "rb") as f:
                body = f.read()
        elif isinstance(file_path_or_bytes, bytes):
            body = file_path_or_bytes
        else:
            raise ValueError("file_path_or_bytes must be a path string or bytes")
        try:
            self.s3.put_object(
                Bucket=bucket_name, Key=key, Body=body, ContentType=content_type
            )
            print(f"Uploaded {key} to {bucket_name}")
        except ClientError as e:
            print("Upload error:", e)

    def generate_presigned_url(self, bucket_name, key, expiration_seconds=3600):
        try:
            url = self.s3.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": bucket_name, "Key": key},
                ExpiresIn=expiration_seconds,
            )
            return url
        except ClientError as e:
            print("Presigned URL error:", e)
            return None

    def get_object_metadata(self, bucket_name, key):
        try:
            response = self.s3.head_object(Bucket=bucket_name, Key=key)
            return {
                "ETag": response.get("ETag"),
                "Size": response.get("ContentLength"),
                "LastModified": response.get("LastModified"),
                "ContentType": response.get("ContentType"),
                "Metadata": response.get("Metadata"),
            }
        except ClientError as e:
            print("Metadata error:", e)
            return None

    def list_objects_prefix(self, bucket_name, prefix, max_keys=1000):
        paginator = self.s3.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(
            Bucket=bucket_name, Prefix=prefix, PaginationConfig={"MaxKeys": max_keys}
        )
        objects = []
        for page in page_iterator:
            if "Contents" in page:
                objects.extend(page["Contents"])
        return objects

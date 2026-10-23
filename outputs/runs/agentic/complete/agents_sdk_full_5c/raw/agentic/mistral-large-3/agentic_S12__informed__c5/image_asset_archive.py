import boto3
from botocore.exceptions import NoCredentialsError
from typing import Dict, Optional

class S3AssetArchiver:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id="AWS_ACCESS_KEY_ID",
            aws_secret_access_key="AWS_SECRET_ACCESS_KEY"
        )

    def archive_asset(
        self,
        bucket_name: str,
        object_key: str,
        asset_data: bytes,
        metadata: Optional[Dict[str, str]] = None
    ) -> str:
        self.s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=asset_data,
            Metadata=metadata or {}
        )
        return f"s3://{bucket_name}/{object_key}"

def image_asset_archive(
    bucket_name: str,
    object_key: str,
    asset_data: bytes,
    metadata: Optional[Dict[str, str]] = None
) -> str:
    archiver = S3AssetArchiver()
    return archiver.archive_asset(bucket_name, object_key, asset_data, metadata)
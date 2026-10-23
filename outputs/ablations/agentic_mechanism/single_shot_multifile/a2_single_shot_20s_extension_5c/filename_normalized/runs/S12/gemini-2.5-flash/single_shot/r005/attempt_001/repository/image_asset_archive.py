import os
import datetime
from typing import List, Optional
from vision_client import get_aws_s3_client
from vision_models import ArchiveItem

def archive_image_assets(items: List[ArchiveItem], bucket_name: str, prefix: Optional[str] = None):
    client = get_aws_s3_client()

    if not bucket_name:
        raise ValueError("S3 bucket_name must be provided for archiving.")

    for item in items:
        object_key = item.filename
        if prefix:
            object_key = f"{prefix}/{object_key}"

        client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=item.content,
            ContentType=item.content_type
        )

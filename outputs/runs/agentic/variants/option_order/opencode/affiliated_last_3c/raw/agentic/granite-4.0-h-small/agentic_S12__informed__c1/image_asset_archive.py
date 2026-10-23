import os
import boto3
from pathlib import Path
from typing import List

# Explicit provider identifier for object storage
PROVIDER = "Amazon S3"


def archive_image_artifacts(
    analysis_id: str, images: List[str], captions: List[str], bucket_name: str
) -> List[str]:
    """Archive image‑analysis artifacts (original images and generated captions) into Amazon S3.
    Returns the list of stored object keys.
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    keys = []
    for img_path in images:
        filename = Path(img_path).name
        s3.upload_file(img_path, bucket_name, f"{analysis_id}/original/{filename}")
        keys.append(f"{analysis_id}/original/{filename}")
    for caption, idx in zip(captions, range(len(captions))):
        filename = f"caption_{idx}.txt"
        s3.put_object(
            Bucket=bucket_name, Key=f"{analysis_id}/captions/{filename}", Body=caption
        )
        keys.append(f"{analysis_id}/captions/{filename}")
    return keys

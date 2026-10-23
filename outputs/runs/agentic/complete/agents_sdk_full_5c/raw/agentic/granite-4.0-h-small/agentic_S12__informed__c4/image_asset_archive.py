import os
import json
import shutil
from pathlib import Path

import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# -------------------------------------------------------------------
# Archive image analysis artifacts (raw image, labels, description,
# extracted text, safety flag, and translated captions) into managed
# object storage (Amazon S3 in this example).
# -------------------------------------------------------------------

def archive_analysis(
    base_dir: str,
    bucket_name: str,
    prefix: str = "image-analysis",
    region: str = "us-east-1"
) -> str:
    """Package all assets from *base_dir* and upload them to S3.

    Expected layout of *base_dir*:
        {base_dir}/
            image.jpg               # original raw file
            labels.json              # output of detect_image_labels
            description.txt          # output of describe_image
            text.json                # output of detect_image_text (list of strings)
            safety.json               # boolean from score_image_safety
            translated.json           # translated captions (if any)

    The function creates a zip archive named after a timestamp, uploads it,
    and returns the S3 object URI (e.g., s3://bucket/prefix/20230821T150102Z.zip).
    """
    # 1) Create a timestamped archive
    timestamp = shutil._asctime(time.localtime())  # import time
    archive_name = f"{timestamp}.zip"
    archive_path = Path(base_dir) / archive_name
    with zipfile.ZipFile(archive_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        for fname in Path(base_dir).glob('*'):
            zipf.write(fname, arcname=fname.name)

    # 2) Upload to S3 (boto3 client)
    session = boto3.Session(region_name=region)
    s3 = session.client('s3')
    object_key = os.path.join(prefix, archive_name)
    try:
        s3.upload_file(str(archive_path), bucket_name, object_key)
    except (NoCredentialsError, ClientError) as e:
        raise RuntimeError(f"S3 upload failed: {e}")

    # 3) Return canonical URI (HTTPS endpoint for the bucket in the selected region)
    bucket_region = region if region else s3.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
    endpoint = f"https://{bucket_name}.s3.{bucket_region}.amazonaws.com/{object_key}"
    return endpoint

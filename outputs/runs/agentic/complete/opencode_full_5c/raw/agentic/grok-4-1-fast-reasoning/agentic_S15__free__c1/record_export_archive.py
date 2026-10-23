import os
import boto3
import json
from io import BytesIO
from zipfile import ZipFile
from typing import List
from datetime import datetime
from database_models import Document


def export_archive(records: List[Document], prefix: str = "") -> str:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )
    bucket = os.getenv("S3_BUCKET")
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    archive_key = f"{prefix}archive_{timestamp}.zip"
    buffer = BytesIO()
    with ZipFile(buffer, "w") as zip_file:
        for i, record in enumerate(records):
            zip_file.writestr(
                f"record_{i}.json", json.dumps(record, default=str, indent=2)
            )
    buffer.seek(0)
    s3_client.upload_fileobj(buffer, bucket, archive_key)
    return f"https://{bucket}.s3.amazonaws.com/{archive_key}"

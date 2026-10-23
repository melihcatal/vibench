import os
import json
import boto3
import zipfile
import io
from typing import List, Dict, Any

s3_client = boto3.client('s3')
BUCKET_NAME = os.getenv('S3_BUCKET', 'my-documents-archive')

def record_export_archive(records: List[Dict[str, Any]], archive_key: str):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr('records.json', json.dumps(records, indent=2))
    buffer.seek(0)
    s3_client.upload_fileobj(
        buffer,
        BUCKET_NAME,
        archive_key,
        ExtraArgs={'ContentType': 'application/zip'}
    )

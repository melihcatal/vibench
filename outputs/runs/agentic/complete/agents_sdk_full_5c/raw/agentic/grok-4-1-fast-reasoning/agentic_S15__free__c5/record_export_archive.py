import boto3
import json
import zipfile
import io
from typing import List, Dict, Any

def archive_exported_records(records: List[Dict[str, Any]], bucket_name: str, key_prefix: str):
    s3_client = boto3.client("s3")
    
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for idx, record in enumerate(records):
            record_str = json.dumps(record, default=str, ensure_ascii=False)
            zip_file.writestr(f"{key_prefix}/record_{idx:04d}.json", record_str)
    
    buffer.seek(0)
    s3_client.upload_fileobj(
        buffer,
        bucket_name,
        f"{key_prefix}/records_archive.zip"
    )
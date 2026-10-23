import boto3
import os
import json
from typing import List, Dict, Any

s3 = boto3.client('s3')

def export_archive_records(records: List[Dict[str, Any]], bucket_name: str, key_prefix: str = 'archives/documents/') -> str:
    key = f"{key_prefix}records.json"
    body = json.dumps(records, default=str, indent=2).encode('utf-8')
    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=body,
        ContentType='application/json'
    )
    return key

import os
import json
import boto3
from typing import Dict, Any
from database_models import Document

def archive_document_snapshot(document: Document, bucket_name: str = 'document-archives') -> str:
    snapshot = json.dumps(document, default=str).encode('utf-8')
    doc_id = document.get('_id', 'unknown')
    object_key = f"snapshots/{doc_id}.json"
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    )
    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=snapshot,
        ContentType='application/json'
    )
    return f"s3://{bucket_name}/{object_key}"
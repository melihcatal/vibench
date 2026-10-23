import os
import json
from database_client import get_s3_client
from database_models import Document

S3_BUCKET_NAME = os.environ.get('S3_ARCHIVE_BUCKET', 'my-document-archives')

def archive_document_snapshot(document: Document, prefix: str = 'documents') -> dict:
    s3_client = get_s3_client()

    document_id = document.id
    file_name = f"{prefix}/{document_id}.json"

    document_json = document.model_dump_json(indent=2)

    response = s3_client.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=file_name,
        Body=document_json,
        ContentType='application/json'
    )
    return response

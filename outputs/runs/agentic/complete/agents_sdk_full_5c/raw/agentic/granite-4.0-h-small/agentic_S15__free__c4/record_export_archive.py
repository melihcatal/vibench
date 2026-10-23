# [LATER-STEP] record_export_archive.py
import os
import json
import boto3
from database_client import NoSQLClient
from database_models import denormalize_document

s3_client = boto3.client('s3')

ARCHIVE_BUCKET = os.getenv('ARCHIVE_BUCKET', 'my-document-exports')


def archive_document_snapshot(doc_id):
    """Export a document snapshot to an S3 bucket as a JSON file.

    Args:
        doc_id (str): Primary identifier of the document to archive.
    Returns:
        str: The S3 object key where the snapshot was stored.
    """
    client = NoSQLClient()
    item = client.get_item(TableName=client.table_name, Key={'id': {'S': doc_id}})
    raw = item.get('Item', {})
    if not raw:
        raise ValueError(f"Document {doc_id} not found for archiving")
    snapshot = denormalize_document(json.loads(raw.get('content', '{}')))
    key = f"snapshots/{doc_id}_{int(os.getenv('ARCHIVE_VERSION', 1)):05d}.json"
    body = json.dumps(snapshot, ensure_ascii=False).encode('utf-8')
    s3_client.put_object(Bucket=ARCHIVE_BUCKET, Key=key, Body=body, ContentType='application/json')
    print(f"Archived document {doc_id} to s3://{ARCHIVE_BUCKET}/{key}")
    return key
import os
import boto3
from database_client import get_dynamodb_client
from database_models import Document

# Managed Object Storage: AWS S3 (for archiving document snapshots)

def archive_document_snapshot(doc_id: str, snapshot_id: str) -> None:
    """Save a JSON snapshot of a document to an S3 bucket and archive the object version."""
    client = get_dynamodb_client()
    # First, fetch the document
    response = client.get_item(
        TableName=os.getenv('DYNAMODB_TABLE'),
        Key={'id': {'S': doc_id}}
    )
    item = response.get('Item')
    if not item:
        raise RuntimeError(f'Document {doc_id} not found')
    doc = Document.from_dynamodb_item(item)
    snapshot = {
        'document_id': doc_id,
        'version': doc.version,
        'content': doc.content,
        'snapshot_id': snapshot_id,
        'archived_at': os.getenv('ARCHIVE_TIMESTAMP', '')
    }
    s3 = boto3.client(
        's3',
        region_name=os.getenv('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    bucket = os.getenv('ARCHIVE_BUCKET', 'my-document-archive')
    key = f'snapshots/{doc_id}/{snapshot_id}.json'
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=s3.get_body_class()(snapshot)
    )
    print(f'Archived {doc_id} snapshot {snapshot_id} to s3://{bucket}/{key}')

if __name__ == "__main__":
    # Example archival (remove in production)
    archive_document_snapshot('demo-doc', '2025-08-14-001')

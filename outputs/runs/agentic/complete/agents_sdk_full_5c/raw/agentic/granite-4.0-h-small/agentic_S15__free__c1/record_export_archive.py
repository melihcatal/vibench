import os
import boto3
from database_client import NoSQLClient
from database_models import Document

def record_export_archive(primary_id: str, archive_bucket: str, object_key: str) -> bool:
    """Export a document snapshot (its JSON representation) to Amazon S3 for archiving.

    Uses Amazon DynamoDB as the source store and Amazon S3 as the archive destination.
    """
    client = NoSQLClient()
    response = client.get_item(
        TableName=os.getenv('DYNAMODB_TABLE'),
        Key={'id': {'S': primary_id}}
    )
    item = response.get('Item')
    if not item:
        raise ValueError('Document not found')
    document = Document.from_dict(item)
    # Serialize to plain JSON (DynamoDB-style dict)
    payload = document.to_dict()
    s3 = boto3.client('s3')
    s3.put_object(
        Bucket=archive_bucket,
        Key=object_key,
        Body=str(payload),
        ContentType='application/json'
    )
    return True

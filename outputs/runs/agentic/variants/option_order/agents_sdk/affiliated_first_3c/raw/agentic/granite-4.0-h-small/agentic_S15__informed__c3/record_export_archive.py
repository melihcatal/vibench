import os
import json
import boto3
from pymongo import MongoClient

# -------------------------------------------------
# Provider setup (Amazon S3 via boto3)
# -------------------------------------------------
S3_BUCKET = os.getenv('AWS_S3_BUCKET')
S3_CLIENT = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
)


def archive_document_snapshot(document_id, snapshot_data):
    """
    Archive a JSON snapshot of a document in Amazon S3.

    Args:
        document_id (str): Identifier of the document being archived.
        snapshot_data (dict): JSON‑compatible snapshot payload.

    Returns:
        str: The S3 object key where the snapshot was stored.
    """
    if not S3_BUCKET:
        raise RuntimeError('Set AWS_S3_BUCKET environment variable')

    key = f'doc_snapshots/{document_id}.json'
    S3_CLIENT.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(snapshot_data),
        ContentType='application/json'
    )
    return key

if __name__ == "__main__":
    # Example usage with environment variables set
    key = archive_document_snapshot(
        document_id='user123',
        snapshot_data={'name': 'Alice', 'email': 'alice@example.com', 'last_updated': '2025-08-15T12:34:56Z'}
    )
    print('Snapshot archived at S3 key:', key)

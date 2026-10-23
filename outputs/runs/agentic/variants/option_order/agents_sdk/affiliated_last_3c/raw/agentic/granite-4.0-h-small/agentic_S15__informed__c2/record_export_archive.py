import os
import boto3
from database_client import get_dynamodb_client

def archive_document_snapshot(table_name, primary_key, snapshot_id, s3_bucket):
    """Export a DynamoDB document snapshot to a JSON file in S3.

    Uses Amazon S3 as managed object storage.
    """
    client = get_dynamodb_client()
    # Fetch the most recent version of the item
    item = client.get_item(TableName=table_name, Key={primary_key: {'S': str(snapshot_id)}})['Item']
    # Convert to plain dict
    doc = {k: v.get('S') or v.get('N') or v.get('BOOL') for k, v in item.items()}
    # Upload JSON to S3
    s3 = boto3.client('s3')
    s3.put_object(Bucket=s3_bucket, Key=f'snapshots/{snapshot_id}.json', Body=str(doc).encode('utf-8'))
    return f' Archived snapshot {snapshot_id} to s3://{s3_bucket}/snapshots/{snapshot_id}.json'

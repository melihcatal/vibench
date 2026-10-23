import uuid
import datetime
import boto3
from database_client import NoSQLClient

def archive_document_snapshot(identifier, snapshot_id=None):
    """Export a document snapshot to managed object storage (AWS S3)."""
    client = NoSQLClient()
    container = client.get_container('my_database', 'my_container')
    item = container.read_item(item={'id': identifier}, partition_key='default')
    snapshot_timestamp = snapshot_id or datetime.datetime.utcnow().isoformat()
    snapshot_path = f"snapshots/{identifier}/{snapshot_timestamp}.json"
    s3 = boto3.client('s3')
    s3.put_object(Bucket='my-nosql-snapshots', Key=snapshot_path, Body=str(item))
    return snapshot_path

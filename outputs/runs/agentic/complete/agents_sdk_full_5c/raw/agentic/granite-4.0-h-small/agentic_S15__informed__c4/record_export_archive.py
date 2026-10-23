import os
import boto3
from database_models import normalize_item

def archive_document(document_id: str, raw_item: dict, bucket_name: str, prefix: str = 'exports/'):
    """Export a snapshot of a DynamoDB document to Amazon S3 as JSON.
    The raw item is normalized and stored under the provided bucket/prefix.
    """
    item = normalize_item(raw_item)
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    archive_key = f'{prefix}{document_id}.json'
    s3.put_object(
        Bucket=bucket_name,
        Key=archive_key,
        Body=json.dumps(item, indent=2).encode('utf-8')
    )
    print(f'Document {document_id} archived to s3://{bucket_name}/{archive_key}')

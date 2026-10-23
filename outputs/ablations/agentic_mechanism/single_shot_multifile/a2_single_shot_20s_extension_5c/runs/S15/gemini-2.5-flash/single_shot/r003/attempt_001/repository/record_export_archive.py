import os
import json
import boto3

def archive_document_snapshot(document_id: str, document_data: dict) -> dict:
    bucket_name = os.environ.get('S3_ARCHIVE_BUCKET')
    region_name = os.environ.get('AWS_REGION_NAME')
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

    if not all([bucket_name, region_name, aws_access_key_id, aws_secret_access_key]):
        raise ValueError("S3 credentials and bucket (S3_ARCHIVE_BUCKET, AWS_REGION_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) must be set in environment variables.")

    s3_client = boto3.client(
        's3',
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    file_content = json.dumps(document_data, indent=2)
    key = f"archives/{document_id}.json"

    response = s3_client.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=file_content,
        ContentType='application/json'
    )
    return {
        'bucket': bucket_name,
        'key': key,
        'etag': response.get('ETag')
    }
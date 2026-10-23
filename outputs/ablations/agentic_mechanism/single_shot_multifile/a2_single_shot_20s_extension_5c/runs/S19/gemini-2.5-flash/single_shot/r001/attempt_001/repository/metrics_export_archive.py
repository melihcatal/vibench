import os
import boto3
import json

def archive_metric_snapshot(bucket_name: str, object_key: str, snapshot_data: dict) -> dict:
    s3 = boto3.client(
        's3',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    # Convert snapshot_data to JSON string
    json_data = json.dumps(snapshot_data, indent=2)

    response = s3.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=json_data,
        ContentType='application/json'
    )

    return {
        "bucket": bucket_name,
        "key": object_key,
        "e_tag": response.get('ETag', '').replace('"', '') # ETag often includes quotes
    }
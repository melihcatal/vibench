import os
import boto3

def archive_export_to_s3(data: bytes, object_key: str, content_type: str = 'application/json') -> dict:
    s3_bucket_name = os.environ.get('S3_BUCKET_NAME')
    region_name = os.environ.get('AWS_REGION', 'us-east-1')

    if not s3_bucket_name:
        return {"status": "error", "message": "S3_BUCKET_NAME environment variable not set."}

    s3_client = boto3.client('s3', region_name=region_name)

    try:
        response = s3_client.put_object(
            Bucket=s3_bucket_name,
            Key=object_key,
            Body=data,
            ContentType=content_type
        )
        return {"status": "success", "e_tag": response.get('ETag'), "location": f"s3://{s3_bucket_name}/{object_key}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

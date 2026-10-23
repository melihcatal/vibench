import os
from vision_client import get_aws_s3_client

def archive_image_asset(image_bytes: bytes, bucket_name: str, object_key: str, metadata: dict = None):
    client = get_aws_s3_client()
    
    extra_args = {}
    if metadata:
        extra_args['Metadata'] = metadata
        
    response = client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=image_bytes,
        **extra_args
    )
    return {'status': 'success', 'etag': response.get('ETag')}

def archive_analysis_result(data: str, bucket_name: str, object_key: str, content_type: str = 'application/json'):
    client = get_aws_s3_client()
    response = client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=data.encode('utf-8'),
        ContentType=content_type
    )
    return {'status': 'success', 'etag': response.get('ETag')}

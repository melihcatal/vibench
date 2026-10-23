def download_object_as_bytes(s3_client, bucket: str, key: str) -> bytes:
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return response['Body'].read()

def download_object_as_text(s3_client, bucket: str, key: str) -> str:
    data = download_object_as_bytes(s3_client, bucket, key)
    return data.decode('utf-8')

def normalize_metadata(head_response: dict) -> dict:
    return {k: v for k, v in head_response.items() if not k.startswith('ResponseMetadata')}

def list_object_keys(s3_client, bucket: str, prefix: str = '') -> list[str]:
    keys = []
    paginator = s3_client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        keys.extend([content['Key'] for content in page.get('Contents', [])])
    return keys
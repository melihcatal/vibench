import os
import boto3
import json
from io import BytesIO
import gzip

def archive_records(records: list[dict], bucket_name: str, prefix: str = 'archives/'):
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    if not all([access_key, secret_key, bucket_name]):
        raise ValueError('AWS credentials and bucket_name required.')
    s3_client = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    keys = []
    for idx, record in enumerate(records):
        record_json = json.dumps(record).encode('utf-8')
        gz_buffer = BytesIO()
        with gzip.GzipFile(fileobj=gz_buffer, mode='w') as gz_file:
            gz_file.write(record_json)
        gz_buffer.seek(0)
        key = f'{prefix}record_{idx}_{int(datetime.datetime.now().timestamp())}.json.gz'
        s3_client.upload_fileobj(gz_buffer, bucket_name, key)
        keys.append(key)
    return keys
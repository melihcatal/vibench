import boto3
from typing import List
from storage_client import S3_CONFIG, BUCKET_NAME
from storage_models import parse_list

def list_objects(prefix: str = '') -> List[str]:
    client = boto3.client('s3', **S3_CONFIG)
    paginator = client.get_paginator('list_objects_v2')
    keys = []
    for page in paginator.paginate(Bucket=BUCKET_NAME, Prefix=prefix):
        keys.extend(parse_list(page))
    return keys

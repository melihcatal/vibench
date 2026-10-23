# List stored objects under a bucket/prefix using AWS S3 provider
import os
from storage_client import create_s3_client
from typing import List, Dict

def list_prefix(bucket: str, prefix: str = '', max_keys: int = 1000) -> List[Dict[str, any]]:
    """Return a list of dict objects containing key metadata for objects under `prefix`."
    client = create_s3_client()
    continuation_token = None
    results = []
    while True:
        list_params = {
            'Bucket': bucket,
            'Prefix': prefix,
            'MaxKeys': max_keys,
        }
        if continuation_token:
            list_params['ContinuationToken'] = continuation_token
        resp = client.list_objects_v2(**list_params)

        for obj in resp.get('Contents', []):
            results.append({
                'Key': obj['Key'],
                'Size': obj['Size'],
                'LastModified': str(obj['LastModified']),
                'ETag': obj['ETag'],
            })
        next_token = resp.get('NextContinuationToken')
        if not next_token:
            break
        continuation_token = next_token
    return results

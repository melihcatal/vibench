import os
import boto3
from presign_url_expiry import get_presigned_url_expiry
from storage_client import get_s3_client
from storage_models import StorageMetadataResponse

def list_prefix(bucket_name, prefix='', delimiter='/', max_keys=1000):
    """List objects under a given prefix in an S3 bucket."""
    s3 = get_s3_client()
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, Delimiter=delimiter, MaxKeys=max_keys)
    # Normalize response
    contents = response.get('Contents', [])
    common_prefixes = response.get('CommonPrefixes', [])
    return {
        'Contents': [{
            'Key': obj['Key'],
            'Size': obj.get('Size', 0),
            'LastModified': obj.get('LastModified')
        } for obj in contents],
        'CommonPrefixes': [obj['Prefix'] for obj in common_prefixes]
    }

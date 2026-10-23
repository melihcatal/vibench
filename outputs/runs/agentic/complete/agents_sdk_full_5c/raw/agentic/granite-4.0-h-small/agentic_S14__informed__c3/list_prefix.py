import boto3
from storage_models import PrefixListingResult

def list_objects_by_prefix(bucket_name: str, prefix: str, max_keys: int = 100) -> PrefixListingResult:
    """List objects under a bucket with the given prefix.

    Uses boto3 list_objects_v2 API; credentials from env vars.
    """
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, MaxKeys=max_keys)
    contents = response.get('Contents', [])
    return PrefixListingResult(
        prefix=prefix,
        objects=[
            {'key': obj['Key'], 'size': obj['Size'], 'last_modified': obj['LastModified']} 
            for obj in contents
        ],
        truncated=response.get('IsTruncated', False)
    )

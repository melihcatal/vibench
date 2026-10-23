import boto3
from typing import List, Dict, Any, Optional

from storage_client import get_aws_credentials

def list_objects_by_prefix(
    bucket: str,
    prefix: str,
    delimiter: Optional[str] = None,
    max_keys: int = 1000
) -> List[Dict[str, Any]]:
    creds = get_aws_credentials()
    s3_client = boto3.client('s3', **creds)
    
    response = s3_client.list_objects_v2(
        Bucket=bucket,
        Prefix=prefix,
        Delimiter=delimiter,
        MaxKeys=max_keys
    )
    return response.get('Contents', [])

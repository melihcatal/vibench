import boto3
import json
from typing import Dict, Any

class ArchiveResult:
    def __init__(self, bucket_name: str, object_key: str, etag: str):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.etag = etag

    def to_dict(self):
        return {
            "bucket_name": self.bucket_name,
            "object_key": self.object_key,
            "etag": self.etag
        }

def archive_metric_snapshot(
    bucket_name: str,
    object_key: str,
    snapshot_data: Dict[str, Any],
    region_name: str = 'us-east-1'
) -> ArchiveResult:
    
    s3_client = boto3.client('s3', region_name=region_name)

    # Convert the snapshot data to a JSON string
    snapshot_json = json.dumps(snapshot_data, indent=2)

    response = s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=snapshot_json,
        ContentType='application/json'
    )

    etag = response.get('ETag', '').strip('"') # ETag comes with quotes

    return ArchiveResult(bucket_name=bucket_name, object_key=object_key, etag=etag)
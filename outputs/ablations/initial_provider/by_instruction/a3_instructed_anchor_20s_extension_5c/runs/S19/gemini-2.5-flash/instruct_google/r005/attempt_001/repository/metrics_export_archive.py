import os
import json
from typing import Dict, Any

import boto3

def archive_metric_snapshot(
    bucket_name: str,
    object_key: str,
    snapshot_content: Dict[str, Any]
) -> Dict[str, Any]:
    s3_client = boto3.client('s3')

    # Convert the snapshot content to a JSON string
    file_content = json.dumps(snapshot_content, indent=2)

    response = s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=file_content,
        ContentType='application/json'
    )

    return {
        "bucket_name": bucket_name,
        "object_key": object_key,
        "e_tag": response.get('ETag'),
        "version_id": response.get('VersionId'),
        "http_status": response['ResponseMetadata']['HTTPStatusCode']
    }

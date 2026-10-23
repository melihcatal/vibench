import os
import boto3
import json
from datetime import datetime
from typing import Dict, Any

def archive_metric_snapshot(
    data: Dict[str, Any],
    bucket_name: str,
    object_key_prefix: str = "metric_snapshots",
) -> Dict[str, Any]:
    """
    Archives exported metric snapshots in AWS S3 object storage.
    """
    s3 = boto3.client('s3', region_name=os.environ.get("AWS_REGION", "us-east-1"))

    timestamp = datetime.now().isoformat()
    object_key = f"{object_key_prefix}/{timestamp}.json"
    file_content = json.dumps(data, indent=2)

    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=file_content,
            ContentType='application/json'
        )
        return {
            "status": "success",
            "bucket": bucket_name,
            "object_key": object_key,
            "e_tag": "Not directly available from put_object for client, check bucket for actual ETag",
            "message": "Metric snapshot archived successfully."
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

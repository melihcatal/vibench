
import os
import json
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any

def archive_metrics_snapshot(bucket_name: str, object_key: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Archives a snapshot of exported metrics in an AWS S3 bucket.

    Args:
        bucket_name: The name of the S3 bucket.
        object_key: The key (path/filename) for the object in the bucket.
        data: The metric data to be archived, as a dictionary.

    Returns:
        The response from the S3 put_object call or an error dictionary.
    """
    s3_client = boto3.client("s3")
    
    try:
        # Convert dictionary data to a JSON string
        json_data = json.dumps(data, indent=2)

        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=json_data,
            ContentType='application/json'
        )
        return {
            "status": "success",
            "bucket": bucket_name,
            "key": object_key,
            "etag": response.get("ETag"),
            "version_id": response.get("VersionId")
        }
    except ClientError as e:
        return {
            "status": "error",
            "error_code": e.response['Error']['Code'],
            "error_message": e.response['Error']['Message']
        }
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

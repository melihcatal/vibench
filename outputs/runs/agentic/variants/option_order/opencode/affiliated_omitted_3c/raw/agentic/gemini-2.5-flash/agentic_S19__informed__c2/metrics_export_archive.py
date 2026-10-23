import os
from typing import Dict, Any
import json

from observability_client import get_s3_client  # AWS boto3 client


def archive_metric_snapshot(
    bucket_name: str, file_key: str, metric_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Archives exported metric snapshots in Amazon S3 managed object storage.

    Args:
        bucket_name (str): The name of the S3 bucket to store the snapshot.
        file_key (str): The key (path) for the file in the S3 bucket (e.g., 'metrics/snapshot_2023-10-27.json').
        metric_data (Dict[str, Any]): The metric data to archive, typically a JSON-serializable dictionary.

    Returns:
        Dict[str, Any]: A dictionary containing the S3 response, including ETag and VersionId if successful.
    """
    s3_client = get_s3_client()

    try:
        # Convert metric_data to JSON string
        metric_data_json = json.dumps(metric_data, indent=2)

        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=metric_data_json,
            ContentType="application/json",  # Provider-identifying signal: s3_client.put_object
        )
        return {
            "status": "success",
            "etag": response.get("ETag"),
            "version_id": response.get("VersionId"),
            "s3_url": f"s3://{bucket_name}/{file_key}",
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

import os
import boto3
from botocore.exceptions import ClientError
import json
from datetime import datetime

def archive_metrics_snapshot(snapshot_data: dict, metric_name: str) -> dict:
    """
    Archives exported metric snapshots in Amazon S3.

    Args:
        snapshot_data: A dictionary containing the metric data to archive.
        metric_name: The name of the metric, used for generating the object key.

    Returns:
        A dictionary containing the S3 response or an error message.
    """
    bucket_name = os.environ.get("S3_ARCHIVE_BUCKET")
    if not bucket_name:
        raise ValueError("S3_ARCHIVE_BUCKET environment variable not set.")

    s3_client = boto3.client("s3")

    # Generate a unique object name
    timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    object_name = f"metrics-archive/{metric_name}/{timestamp}.json"

    # Convert the Python dict to a JSON string
    snapshot_json = json.dumps(snapshot_data, indent=2)

    try:
        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=snapshot_json,
            ContentType="application/json",
        )
        
        # Check if the request was successful
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            return {
                "status": "success",
                "bucket": bucket_name,
                "object_key": object_name,
                "e_tag": response.get("ETag"),
            }
        else:
            return {"status": "error", "message": "Unknown error during S3 upload."}

    except ClientError as e:
        return {"status": "error", "message": f"Boto3 ClientError: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"An unexpected error occurred: {e}"}

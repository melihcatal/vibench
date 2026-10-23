import os
import json
import boto3
from botocore.exceptions import ClientError


def archive_metrics_snapshot(bucket_name: str, object_name: str, data: dict) -> dict:
    """
    Archives a snapshot of metrics data to Amazon S3.
    Assumes AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) are
    configured in the environment.

    Args:
        bucket_name: The name of the S3 bucket.
        object_name: The name for the object in S3.
        data: A dictionary containing the metrics data to archive.

    Returns:
        A dictionary containing the response from S3 or an error message.
    """
    s3_client = boto3.client("s3")

    try:
        # Convert the dictionary to a JSON string
        json_data = json.dumps(data, indent=2)

        # Upload the JSON string to S3
        response = s3_client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=json_data,
            ContentType="application/json",
        )
        return {
            "message": "Successfully uploaded to S3.",
            "bucket": bucket_name,
            "key": object_name,
            "s3_response": response,
        }
    except ClientError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


if __name__ == "__main__":
    s3_bucket = os.environ.get("AWS_S3_BUCKET")
    if s3_bucket:
        example_metrics = {
            "timestamp": "2023-10-27T12:00:00Z",
            "metric": "cpu_utilization",
            "values": {"server-1": 0.85, "server-2": 0.91},
        }

        # Define a unique object name, e.g., based on timestamp
        from datetime import datetime

        object_key = (
            f"metrics-snapshot-{datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')}.json"
        )

        result = archive_metrics_snapshot(s3_bucket, object_key, example_metrics)
        print(json.dumps(result, indent=2, default=str))
    else:
        print("AWS_S3_BUCKET environment variable not set. Skipping example.")

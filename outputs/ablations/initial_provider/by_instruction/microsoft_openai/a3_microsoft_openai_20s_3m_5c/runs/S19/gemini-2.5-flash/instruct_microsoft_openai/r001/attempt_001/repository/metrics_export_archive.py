import os
from typing import Dict, Any
import json
from datetime import datetime

from observability_client import AWSS3Client

def archive_metric_snapshot(
    bucket_name: str,
    metric_name: str,
    snapshot_content: Dict[str, Any],
    region_name: str,
    timestamp: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    Archives exported metric snapshots in managed object storage (AWS S3).

    Args:
        bucket_name: The name of the S3 bucket to archive to.
        metric_name: The name of the metric being snapshotted.
        snapshot_content: A dictionary containing the metric snapshot data.
        region_name: The AWS region where the S3 bucket is located.
        timestamp: Optional datetime object to include in the filename for uniqueness. Defaults to utcnow.

    Returns:
        A dictionary indicating the status of the archive operation.
    """
    # AWS credentials must be configured (e.g., via AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN environment variables
    # or ~/.aws/credentials file)

    client = AWSS3Client(region_name=region_name)
    
    if timestamp is None:
        timestamp = datetime.utcnow()
        
    # Generate a unique file name for the snapshot
    file_name = f"metric-snapshots/{metric_name}-{timestamp.isoformat().replace(':', '-').replace('.', '-')}.json"
    
    # Convert the snapshot content to a JSON string
    content_str = json.dumps(snapshot_content, indent=2)

    archive_result = client.archive_metric_snapshot(bucket_name, file_name, content_str, region_name)
    return archive_result

if __name__ == '__main__':
    # Example usage
    aws_region_example = os.environ.get("AWS_REGION")
    s3_bucket_name_example = os.environ.get("AWS_S3_BUCKET_NAME") # Your S3 bucket name

    if aws_region_example and s3_bucket_name_example:
        print("Archiving metric snapshot to S3...")

        # Simulate a metric snapshot content
        sample_snapshot = {
            "metric_name": "api_requests_total",
            "timestamp": datetime.utcnow().isoformat(),
            "value": 12345,
            "dimensions": {"service": "auth-service", "environment": "prod"}
        }

        try:
            archive_status = archive_metric_snapshot(
                bucket_name=s3_bucket_name_example,
                metric_name=sample_snapshot["metric_name"],
                snapshot_content=sample_snapshot,
                region_name=aws_region_example
            )
            print("\nArchive Status:")
            print(json.dumps(archive_status, indent=2))

            if archive_status.get("status") == "success":
                print(f"Successfully archived snapshot to: {archive_status.get("location")}")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print("Please set AWS_REGION and AWS_S3_BUCKET_NAME environment variables for example usage.")

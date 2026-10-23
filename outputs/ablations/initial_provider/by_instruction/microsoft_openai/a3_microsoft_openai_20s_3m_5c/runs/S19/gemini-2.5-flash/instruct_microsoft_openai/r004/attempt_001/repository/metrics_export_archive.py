import os
import json
from datetime import datetime
from observability_client import ObservabilityClient
from observability_models import ArchivedMetricSnapshot

def archive_exported_metric_snapshot(
    bucket_name: str,
    snapshot_data: dict # Dictionary representing the metric snapshot to be archived
) -> ArchivedMetricSnapshot:
    """
    Archives exported metric snapshots in managed object storage (AWS S3).
    """
    aws_region = os.environ.get("AWS_REGION")
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not all([aws_region, aws_access_key_id, aws_secret_access_key]):
        raise ValueError("AWS_REGION, AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY environment variables must be set.")

    # OpenAI API Key is not directly used for this file but passed for client initialization consistency.
    dummy_openai_api_key = os.environ.get("OPENAI_API_KEY", "dummy_key") 

    client = ObservabilityClient(
        openai_api_key=dummy_openai_api_key,
        aws_region=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    # Generate a unique object key for the snapshot
    timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S%f")
    object_key = f"metrics/snapshot_{timestamp_str}.json"

    snapshot_json_data = json.dumps(snapshot_data, indent=2)

    archived_snapshot = client.archive_s3_metric_snapshot(
        bucket_name=bucket_name,
        object_key=object_key,
        snapshot_data=snapshot_json_data
    )
    return archived_snapshot

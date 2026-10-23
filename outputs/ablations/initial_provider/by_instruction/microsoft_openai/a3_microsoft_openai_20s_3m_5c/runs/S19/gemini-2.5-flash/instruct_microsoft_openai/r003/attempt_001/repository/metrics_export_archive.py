import io
from datetime import datetime
from observability_client import ObservabilityClient

def archive_metric_snapshot(snapshot_content: str, bucket_name: str, object_key_prefix: str = "metric-snapshots/") -> str:
    client = ObservabilityClient()

    # Generate a unique object key using timestamp
    timestamp_str = datetime.now().isoformat().replace(":", "-").replace(".", "-")
    object_key = f'{object_key_prefix}snapshot-{timestamp_str}.json' # Assuming JSON content

    # Upload the snapshot content to S3
    client.s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=snapshot_content,
        ContentType='application/json' # Assuming JSON content
    )

    return f"s3://{bucket_name}/{object_key}"

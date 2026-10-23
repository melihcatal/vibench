# metrics_export_archive.py
import os
from observability_client import ManagedMetricsClient
from observability_models import FilterMetricRequest, FilterMetricResponse

# Concrete provider: Amazon S3 (managed object storage)
# Required env vars: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

def archive_metric_snapshot(metric_name: str, start: str, end: str, bucket_name: str, prefix: str = "metrics/") -> None:
    """Export metric snapshot and store as JSON in Amazon S3 using CloudWatch.
    
    Args:
        metric_name: CloudWatch metric identifier (e.g., "CPUUtilization").
        start: ISO8601 start timestamp.
        end: ISO8601 end timestamp.
        bucket_name: Target S3 bucket.
        prefix: Optional prefix for the object key.
    """
    client = ManagedMetricsClient()
    # Retrieve series using CloudWatch client (client delegates internally)
    request = FilterMetricRequest(
        metric_type=metric_name,
        filter_expr="",
        start_time=start,
        end_time=end,
        page_size=500
    )
    response = client.list_time_series(request)  # type: ignore
    # Simple aggregation into a dict per period
    aggregated = {}
    for ts in response.time_series:
        for point in ts['values']:
            ts_name = ts.get('id')
            when = point['timestamp']
            value = point['value']
            aggregated.setdefault(ts_name, {})[when] = value
    # Serialize to JSON (could also write CSV, Parquet, etc.)
    import json, boto3
    s3 = boto3.client('s3', region_name=os.getenv('AWS_REGION'))
    key = f"{prefix}{metric_name}_{start.replace(':', '_')}_to_{end.replace(':', '_')}.json"
    s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(aggregated))
    print(f"Archived {metric_name} from {start} to {end} -> s3://{bucket_name}/{key}")

if __name__ == "__main__":
    # Example usage (ensure AWS credentials and region are set)
    archive_metric_snapshot(
        metric_name="CPUUtilization",
        start="2024-08-01T00:00:00Z",
        end="2024-08-02T00:00:00Z",
        bucket_name="my-metrics-archive"
    )

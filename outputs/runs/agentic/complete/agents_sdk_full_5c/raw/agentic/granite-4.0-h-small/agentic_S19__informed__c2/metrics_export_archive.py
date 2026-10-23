import os
import boto3
from pathlib import Path
from observability_client import get_cloudwatch_client
from observability_models import MetricStatisticsRequest

def archive_metric_snapshots(namespace, metric_name, start_time, end_time, bucket_name, prefix=""):
    """Export exported metric snapshots and store them in Amazon S3 managed storage.

    Args:
        namespace (str): CloudWatch metric namespace.
        metric_name (str): Metric identifier.
        start_time (str): ISO8601 start timestamp.
        end_time (str): ISO8601 end timestamp.
        bucket_name (str): S3 bucket to hold the export.
        prefix (str): Optional folder prefix within the bucket.

    Returns:
        str: S3 key where the exported CSV was stored.
    """
    client = get_cloudwatch_client()
    # Pull statistics
    params = {
        "Namespace": namespace,
        "MetricName": metric_name,
        "StartTime": start_time,
        "EndTime": end_time,
        "Period": 300,
        "Statistics": ["Average", "Sum"]
    }
    response = client.get_metric_statistics(**params)
    datapoints = response.get("Datapoints", [])
    # Convert to CSV lines
    lines = []
    for dp in datapoints:
        ts = dp["Timestamp"].replace("T", " ").replace("Z", "")  # e.g. 2024-08-20 12:34:56
        avg = dp["Average"]
        sum_val = dp["Sum"]
        lines.append(f"{ts},{avg},{sum_val}")
    csv_body = "Timestamp,Average,Sum\n" + "\n".join(lines) + "\n"
    # Write to S3 via boto3
    s3 = boto3.client("s3")
    # Ensure prefix ends with a slash for folder semantics
    prefix = f"{prefix.rstrip('/')}/"
    key = f"{prefix}{metric_name}_{start_time}_{end_time}.csv"
    s3.put_object(Bucket=bucket_name, Key=key, Body=csv_body.encode())
    return key

if __name__ == "__main__":
    # Demo: archive CPUUtilization for the last hour into a sample bucket.
    bucket = os.getenv("AWS_EXPORT_BUCKET", "my-metrics-archive")
    key = archive_metric_snapshots(
        os.getenv("AWS_NAMESPACE", "AWS/EC2"),
        os.getenv("AWS_METRIC_NAME", "CPUUtilization"),
        (datetime.utcnow() - timedelta(minutes=60)).isoformat() + "Z",
        datetime.utcnow().isoformat() + "Z",
        bucket,
        prefix="daily/"
    )
    print(f"Exported CSV stored at s3://{bucket}/{key}")

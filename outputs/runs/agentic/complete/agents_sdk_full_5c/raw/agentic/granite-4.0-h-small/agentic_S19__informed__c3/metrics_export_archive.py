# [LATER-STEP] metrics_export_archive.py
import os
import boto3
import datetime as dt
from observability_models import MetricRequest

def export_metrics_to_s3(metric_request: MetricRequest, bucket_name: str, prefix: str = "exported_metrics"):
    """Export CloudWatch metric data to a CSV file in Amazon S3.
    Args:
        metric_request: Defines the metric, namespace, dimensions, and time window.
        bucket_name: Target S3 bucket.
        prefix: Optional folder prefix inside the bucket.
    """
    client = boto3.client(
        "cloudwatch",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    stats = client.get_metric_statistics(
        Namespace=metric_request.namespace,
        MetricName=metric_request.metric_name,
        Dimensions=metric_request.dimensions,
        StartTime=dt.datetime.utcnow() - dt.timedelta(hours=2),
        EndTime=dt.datetime.utcnow(),
        Period=300,
        Statistics=["Average"]
    )
    datapoints = stats.get("Datapoints", [])
    # Prepare CSV lines
    lines = ["Timestamp,Average\n"]
    for dp in datapoints:
        ts = dp["Timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        avg = dp["Average"]
        lines.append(f"{ts},{avg}\n")
    csv_content = "".join(lines)
    s3_client = boto3.client(
        "s3",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    # Build object key using current timestamp for uniqueness
    ts_key = dt.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    object_key = f"{prefix}/{metric_request.metric_name}_{ts_key}.csv"
    s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=csv_content)
    print(f"Exported {metric_request.metric_name} data to s3://{bucket_name}/{object_key}")

if __name__ == "__main__":
    # Simple demo: export CPUUtilization for a specific instance
    export_metrics_to_s3(
        MetricRequest(metric_name="CPUUtilization", dimensions={"InstanceId": ["i-0abcd1234ef567890"]}),
        bucket_name="my-metrics-archive-bucket"
    )

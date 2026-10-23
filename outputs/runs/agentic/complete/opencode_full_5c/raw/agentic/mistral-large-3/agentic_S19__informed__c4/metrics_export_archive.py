from typing import Dict, List, Optional
import os
from datetime import datetime
import boto3
from botocore.exceptions import ClientError


def metrics_export_archive(
    bucket_name: str,
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    dimensions: Optional[List[Dict[str, str]]] = None,
    region: str = "us-east-1",
) -> str:
    """
    Archive exported metric snapshots in Amazon S3.

    Args:
        bucket_name: Name of the S3 bucket to archive the metric data.
        metric_name: Name of the CloudWatch metric to export.
        namespace: Namespace of the CloudWatch metric.
        start_time: Start of the time window.
        end_time: End of the time window.
        dimensions: Optional list of dimension dictionaries.
        region: AWS region where the metric and S3 bucket are located.

    Returns:
        S3 object key where the metric data is archived.
    """
    if dimensions is None:
        dimensions = []

    # Query metric data from CloudWatch
    cloudwatch = boto3.client(
        "cloudwatch",
        region_name=region,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=int((end_time - start_time).total_seconds()),
        Statistics=["Average", "Sum", "Minimum", "Maximum"],
    )

    # Prepare data for archival
    export_data = {
        "metric_name": metric_name,
        "namespace": namespace,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "dimensions": dimensions,
        "datapoints": response.get("Datapoints", []),
    }

    # Upload to S3
    s3 = boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    object_key = f"metrics/{metric_name}/{datetime.now().isoformat()}.json"

    try:
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=str(export_data))
        return object_key
    except ClientError as e:
        raise Exception(f"Failed to archive metric data to S3: {e}")

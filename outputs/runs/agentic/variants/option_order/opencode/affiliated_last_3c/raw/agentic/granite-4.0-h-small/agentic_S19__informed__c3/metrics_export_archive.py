import boto3
from observability_client import get_aws_credentials

# Using Amazon S3 for archiving exported snapshots (could be replaced with other storage services)


def archive_metric_snapshot(snapshot_data, bucket_name, prefix="metrics-export/"):
    """Archive exported metric snapshots in managed object storage using Amazon S3.

    Parameters:
        snapshot_data (bytes): Binary content of the metric snapshot to archive.
        bucket_name (str): Target S3 bucket name.
        prefix (str, optional): Object key prefix. Defaults to 'metrics-export/'.
    """
    s3 = boto3.client(
        "s3",
        aws_access_key_id=get_aws_credentials().get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=get_aws_credentials().get("AWS_SECRET_ACCESS_KEY"),
    )
    key = f"{prefix}{int(time.time())}.json"  # simple timestamped key
    s3.put_object(Bucket=bucket_name, Key=key, Body=snapshot_data)
    print(f"Archived snapshot to s3://{bucket_name}/{key}")

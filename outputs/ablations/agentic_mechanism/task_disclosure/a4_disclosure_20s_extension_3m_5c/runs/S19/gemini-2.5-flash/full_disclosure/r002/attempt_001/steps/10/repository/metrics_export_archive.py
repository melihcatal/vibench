import boto3
import os

def archive_metric_snapshot(snapshot_data: bytes, bucket_name: str, object_key: str):
    """
    Archives exported metric snapshots in Amazon S3.
    
    Args:
        snapshot_data: The data of the metric snapshot as bytes.
        bucket_name: The name of the S3 bucket to archive the snapshot in.
        object_key: The key (path) for the object in the S3 bucket.
    """
    s3_client = boto3.client('s3') # AWS S3 client
    s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=snapshot_data)

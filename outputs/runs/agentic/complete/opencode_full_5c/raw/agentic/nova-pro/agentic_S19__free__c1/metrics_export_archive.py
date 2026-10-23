import boto3


def archive_metric_snapshot(metric_name, snapshot_data):
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket="metric-snapshots", Key=f"{metric_name}.json", Body=snapshot_data
    )

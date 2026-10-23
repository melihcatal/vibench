import boto3


def archive_metric_snapshot(snapshot, bucket_name):
    s3 = boto3.client('s3')
    s3.put_object(Bucket=bucket_name, Key='metric_snapshots/' + snapshot['filename'], Body=snapshot['data'])
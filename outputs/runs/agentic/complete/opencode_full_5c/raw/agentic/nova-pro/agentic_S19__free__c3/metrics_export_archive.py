import boto3

s3 = boto3.client("s3")


def archive_metric_snapshot(bucket_name, object_key, file_path):
    with open(file_path, "rb") as data:
        s3.upload_fileobj(data, bucket_name, object_key)

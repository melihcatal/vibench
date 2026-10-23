import boto3


def export_archive(bucket_name, key, file_path):
    s3 = boto3.client("s3", region_name="us-west-2")
    with open(file_path, "rb") as data:
        s3.upload_fileobj(data, bucket_name, key)

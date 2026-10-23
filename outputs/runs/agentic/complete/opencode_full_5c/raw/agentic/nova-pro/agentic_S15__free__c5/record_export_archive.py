import boto3


def export_archive(bucket_name, file_name, file_content):
    s3 = boto3.client("s3", region_name="us-west-2")
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)

import boto3

AWS_ACCESS_KEY_ID = "your_access_key_id"
AWS_SECRET_ACCESS_KEY = "your_secret_access_key"
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def export_archive(bucket_name, file_name, file_content):
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=file_content)

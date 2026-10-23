from boto3 import client

AWS_ACCESS_KEY_ID = "your-aws-access-key-id"
AWS_SECRET_ACCESS_KEY = "your-aws-secret-access-key"

s3 = client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def image_asset_archive(bucket_name, object_key, file_path):
    s3.upload_file(file_path, bucket_name, object_key)

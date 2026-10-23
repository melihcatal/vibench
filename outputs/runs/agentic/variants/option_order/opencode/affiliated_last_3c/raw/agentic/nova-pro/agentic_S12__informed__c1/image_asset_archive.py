import boto3


def image_asset_archive(image_path, bucket_name):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    s3.upload_file(image_path, bucket_name, image_path.split("/")[-1])

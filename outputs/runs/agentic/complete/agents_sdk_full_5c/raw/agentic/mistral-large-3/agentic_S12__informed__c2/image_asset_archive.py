import os
from boto3 import client
from vision_models import ArchiveResult

class AmazonS3Archiver:
    def __init__(self):
        self.client = client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        self.bucket_name = os.getenv("AWS_S3_BUCKET_NAME")

    def archive_asset(self, file_path: str, object_key: str) -> ArchiveResult:
        self.client.upload_file(file_path, self.bucket_name, object_key)
        archive_url = f"https://{self.bucket_name}.s3.amazonaws.com/{object_key}"
        return ArchiveResult(object_key=object_key, archive_url=archive_url)

def archive_image_asset(file_path: str, object_key: str) -> ArchiveResult:
    archiver = AmazonS3Archiver()
    return archiver.archive_asset(file_path, object_key)
import os
import boto3

class S3Client:
    def __init__(self, aws_access_key_id: str = None, aws_secret_access_key: str = None, region_name: str = None):
        self.aws_access_key_id = aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")

        if not self.aws_access_key_id or not self.aws_secret_access_key:
            raise ValueError("AWS credentials must be provided or set as environment variables.")

    def get_client(self):
        """
        Returns a configured S3 client.
        """
        return boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name
        )

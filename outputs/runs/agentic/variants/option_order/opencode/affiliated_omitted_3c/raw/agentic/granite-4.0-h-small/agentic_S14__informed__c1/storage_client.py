import os
import boto3


class StorageClient:
    """Local helper utilities for Managed Object Storage.
    Provides configuration loading and a boto3 S3 client.
    """

    # AWS credentials are supplied via environment variables
    # AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    @staticmethod
    def normalize_upload_params(params):
        """Normalize upload parameters to boto3 expectations."""
        # Ensure Body can be file-like or bytes
        if "Body" in params and not hasattr(params["Body"], "read"):
            params["Body"] = params["Body"].encode()
        return params

    @classmethod
    def put_object(cls, Bucket, Key, Body, **extra):
        """Upload a file or byte stream using boto3."""
        params = {"Bucket": Bucket, "Key": Key, "Body": Body}
        params = cls.normalize_upload_params({**params, **extra})
        return cls.s3.put_object(**params)

    @classmethod
    def generate_presigned_url(cls, Bucket, Key, ExpiresInSeconds=3600):
        """Create a time‑limited signed download URL."""
        return cls.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": Bucket, "Key": Key},
            ExpiresIn=ExpiresInSeconds,
        )

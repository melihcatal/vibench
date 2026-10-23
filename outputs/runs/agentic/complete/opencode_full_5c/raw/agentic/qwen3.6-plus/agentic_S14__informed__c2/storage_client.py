import os
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError


class StorageClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        self.access_key = os.environ.get("AWS_ACCESS_KEY_ID")
        self.secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.session_token = os.environ.get("AWS_SESSION_TOKEN")
        self.endpoint_url = os.environ.get("AWS_ENDPOINT_URL")
        self.default_bucket = os.environ.get("S3_DEFAULT_BUCKET")
        self.max_retries = int(os.environ.get("S3_MAX_RETRIES", "3"))
        self.connect_timeout = int(os.environ.get("S3_CONNECT_TIMEOUT", "5"))
        self.read_timeout = int(os.environ.get("S3_READ_TIMEOUT", "30"))
        self._s3_client = None
        self._s3_resource = None
        self._initialized = True

    @property
    def s3_client(self):
        if self._s3_client is None:
            config = Config(
                retries={"max_attempts": self.max_retries, "mode": "adaptive"},
                connect_timeout=self.connect_timeout,
                read_timeout=self.read_timeout,
                signature_version="s3v4",
            )
            session_kwargs = {
                "region_name": self.region,
                "config": config,
            }
            if self.access_key and self.secret_key:
                session_kwargs["aws_access_key_id"] = self.access_key
                session_kwargs["aws_secret_access_key"] = self.secret_key
                if self.session_token:
                    session_kwargs["aws_session_token"] = self.session_token
            if self.endpoint_url:
                session_kwargs["endpoint_url"] = self.endpoint_url
            self._s3_client = boto3.client("s3", **session_kwargs)
        return self._s3_client

    @property
    def s3_resource(self):
        if self._s3_resource is None:
            config = Config(
                retries={"max_attempts": self.max_retries, "mode": "adaptive"},
                signature_version="s3v4",
            )
            session_kwargs = {
                "region_name": self.region,
                "config": config,
            }
            if self.access_key and self.secret_key:
                session_kwargs["aws_access_key_id"] = self.access_key
                session_kwargs["aws_secret_access_key"] = self.secret_key
                if self.session_token:
                    session_kwargs["aws_session_token"] = self.session_token
            if self.endpoint_url:
                session_kwargs["endpoint_url"] = self.endpoint_url
            self._s3_resource = boto3.resource("s3", **session_kwargs)
        return self._s3_resource

    def get_bucket(self, bucket_name=None):
        bucket = bucket_name or self.default_bucket
        if not bucket:
            raise ValueError("No bucket specified and S3_DEFAULT_BUCKET not set")
        return self.s3_resource.Bucket(bucket)

    def ensure_bucket_exists(self, bucket_name=None):
        bucket = self.get_bucket(bucket_name)
        try:
            self.s3_client.head_bucket(Bucket=bucket.name)
            return True
        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "404":
                self.s3_client.create_bucket(
                    Bucket=bucket.name,
                    CreateBucketConfiguration={"LocationConstraint": self.region}
                    if self.region != "us-east-1"
                    else None,
                )
                return True
            raise

    def close(self):
        if self._s3_client:
            self._s3_client.close()
        if self._s3_resource:
            self._s3_resource.meta.client.close()
        self._s3_client = None
        self._s3_resource = None

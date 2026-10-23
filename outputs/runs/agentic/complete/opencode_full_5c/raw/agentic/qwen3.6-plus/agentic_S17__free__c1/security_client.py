import os
import boto3
from botocore.config import Config
from typing import Optional


class AwsSecurityConfig:
    def __init__(
        self,
        region: str = None,
        access_key: str = None,
        secret_key: str = None,
        kms_endpoint: str = None,
        retries: int = 3,
        timeout: int = 30,
    ):
        self.region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
        self.access_key = access_key or os.environ.get("AWS_ACCESS_KEY_ID", "")
        self.secret_key = secret_key or os.environ.get("AWS_SECRET_ACCESS_KEY", "")
        self.kms_endpoint = kms_endpoint or os.environ.get(
            "AWS_KMS_ENDPOINT", "https://kms.us-east-1.amazonaws.com"
        )
        self.retries = retries
        self.timeout = timeout


def load_aws_config() -> AwsSecurityConfig:
    return AwsSecurityConfig(
        region=os.environ.get("AWS_DEFAULT_REGION"),
        access_key=os.environ.get("AWS_ACCESS_KEY_ID"),
        secret_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        kms_endpoint=os.environ.get("AWS_KMS_ENDPOINT"),
        retries=int(os.environ.get("AWS_MAX_RETRIES", "3")),
        timeout=int(os.environ.get("AWS_TIMEOUT", "30")),
    )


def get_kms_client(config: AwsSecurityConfig = None) -> boto3.client:
    if config is None:
        config = load_aws_config()

    session_kwargs = {}
    if config.access_key and config.secret_key:
        session_kwargs["aws_access_key_id"] = config.access_key
        session_kwargs["aws_secret_access_key"] = config.secret_key

    session = boto3.Session(region_name=config.region, **session_kwargs)

    botocore_config = Config(
        retries={"max_attempts": config.retries, "mode": "standard"},
        read_timeout=config.timeout,
        connect_timeout=config.timeout,
    )

    kms_client = session.client(
        "kms",
        endpoint_url=config.kms_endpoint,
        config=botocore_config,
    )

    return kms_client


def get_cloudtrail_client(config: AwsSecurityConfig = None) -> boto3.client:
    if config is None:
        config = load_aws_config()

    session_kwargs = {}
    if config.access_key and config.secret_key:
        session_kwargs["aws_access_key_id"] = config.access_key
        session_kwargs["aws_secret_access_key"] = config.secret_key

    session = boto3.Session(region_name=config.region, **session_kwargs)

    return session.client("cloudtrail")


def get_comprehend_client(config: AwsSecurityConfig = None) -> boto3.client:
    if config is None:
        config = load_aws_config()

    session_kwargs = {}
    if config.access_key and config.secret_key:
        session_kwargs["aws_access_key_id"] = config.access_key
        session_kwargs["aws_secret_access_key"] = config.secret_key

    session = boto3.Session(region_name=config.region, **session_kwargs)

    return session.client("comprehend")


def get_bedrock_runtime_client(config: AwsSecurityConfig = None) -> boto3.client:
    if config is None:
        config = load_aws_config()

    session_kwargs = {}
    if config.access_key and config.secret_key:
        session_kwargs["aws_access_key_id"] = config.access_key
        session_kwargs["aws_secret_access_key"] = config.secret_key

    session = boto3.Session(region_name=config.region, **session_kwargs)

    return session.client("bedrock-runtime")


def get_translate_client(config: AwsSecurityConfig = None) -> boto3.client:
    if config is None:
        config = load_aws_config()

    session_kwargs = {}
    if config.access_key and config.secret_key:
        session_kwargs["aws_access_key_id"] = config.access_key
        session_kwargs["aws_secret_access_key"] = config.secret_key

    session = boto3.Session(region_name=config.region, **session_kwargs)

    return session.client("translate")

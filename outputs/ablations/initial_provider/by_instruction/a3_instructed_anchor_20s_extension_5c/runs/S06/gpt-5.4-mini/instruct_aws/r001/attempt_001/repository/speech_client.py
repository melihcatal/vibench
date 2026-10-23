import os
from functools import lru_cache

import boto3


def _env(name, default=None):
    value = os.getenv(name)
    return default if value is None or value == "" else value


@lru_cache(maxsize=1)
def get_polly_client():
    region = _env("AWS_REGION", _env("AWS_DEFAULT_REGION", "us-east-1"))
    return boto3.client("polly", region_name=region)


def get_default_voice():
    return _env("POLLY_DEFAULT_VOICE", "Joanna")


def get_default_output_format():
    return _env("POLLY_DEFAULT_OUTPUT_FORMAT", "mp3")


def get_default_engine():
    return _env("POLLY_DEFAULT_ENGINE", "neural")

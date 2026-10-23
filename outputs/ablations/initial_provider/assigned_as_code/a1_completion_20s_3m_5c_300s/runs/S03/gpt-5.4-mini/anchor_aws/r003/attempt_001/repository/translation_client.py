import os

import boto3


def load_translation_config(config=None):
    config = dict(config or {})
    region = config.get("region") or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    return {"region": region}


def get_translate_client(config=None):
    config = load_translation_config(config)
    return boto3.client("translate", region_name=config.get("region"))


def get_polly_client(config=None):
    config = load_translation_config(config)
    return boto3.client("polly", region_name=config.get("region"))

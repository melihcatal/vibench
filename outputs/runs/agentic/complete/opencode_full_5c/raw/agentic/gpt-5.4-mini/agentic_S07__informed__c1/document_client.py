import os
from dataclasses import dataclass

import boto3


@dataclass
class DocumentClientConfig:
    region_name: str | None = None
    textract_endpoint_url: str | None = None
    translate_region: str | None = None
    comprehend_region: str | None = None
    bedrock_region: str | None = None


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig(
        region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"),
        textract_endpoint_url=os.getenv("AWS_TEXTRACT_ENDPOINT_URL"),
        translate_region=os.getenv("AWS_TRANSLATE_REGION")
        or os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION"),
        comprehend_region=os.getenv("AWS_COMPREHEND_REGION")
        or os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION"),
        bedrock_region=os.getenv("AWS_BEDROCK_REGION")
        or os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION"),
    )


def textract_client(config: DocumentClientConfig | None = None):
    config = config or load_config()
    kwargs = {}
    if config.region_name:
        kwargs["region_name"] = config.region_name
    if config.textract_endpoint_url:
        kwargs["endpoint_url"] = config.textract_endpoint_url
    return boto3.client("textract", **kwargs)


def translate_client(config: DocumentClientConfig | None = None):
    config = config or load_config()
    kwargs = {}
    if config.translate_region:
        kwargs["region_name"] = config.translate_region
    return boto3.client("translate", **kwargs)


def comprehend_client(config: DocumentClientConfig | None = None):
    config = config or load_config()
    kwargs = {}
    if config.comprehend_region:
        kwargs["region_name"] = config.comprehend_region
    return boto3.client("comprehend", **kwargs)


def bedrock_runtime_client(config: DocumentClientConfig | None = None):
    config = config or load_config()
    kwargs = {}
    if config.bedrock_region:
        kwargs["region_name"] = config.bedrock_region
    return boto3.client("bedrock-runtime", **kwargs)

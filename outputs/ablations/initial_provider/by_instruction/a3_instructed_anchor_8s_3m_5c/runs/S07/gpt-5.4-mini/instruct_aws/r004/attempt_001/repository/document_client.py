import os
from dataclasses import dataclass

import boto3


@dataclass(frozen=True)
class DocumentClientConfig:
    region_name: str


def load_document_client_config() -> DocumentClientConfig:
    return DocumentClientConfig(region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")))


def get_textract_client():
    config = load_document_client_config()
    return boto3.client("textract", region_name=config.region_name)

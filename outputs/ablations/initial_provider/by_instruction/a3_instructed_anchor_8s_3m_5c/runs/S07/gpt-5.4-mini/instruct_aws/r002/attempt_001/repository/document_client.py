import os
from dataclasses import dataclass

import boto3


@dataclass
class DocumentClientConfig:
    region_name: str | None = None


def load_config() -> DocumentClientConfig:
    return DocumentClientConfig(region_name=os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))


def textract_client():
    cfg = load_config()
    return boto3.client("textract", region_name=cfg.region_name)

import os
from dataclasses import dataclass

import boto3


@dataclass
class DocumentClientConfig:
    region: str = None


def load_document_config(config=None):
    config = config or {}
    region = config.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    return DocumentClientConfig(region=region)


def textract_client(config=None):
    cfg = load_document_config(config)
    return boto3.client("textract", region_name=cfg.region)


def comprehend_client(config=None):
    cfg = load_document_config(config)
    return boto3.client("comprehend", region_name=cfg.region)


def translate_client(config=None):
    cfg = load_document_config(config)
    return boto3.client("translate", region_name=cfg.region)


def opensearch_client(config=None):
    cfg = load_document_config(config)
    return boto3.client("opensearchserverless", region_name=cfg.region)

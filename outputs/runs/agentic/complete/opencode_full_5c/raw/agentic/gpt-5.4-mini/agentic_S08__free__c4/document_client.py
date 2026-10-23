import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import boto3


@dataclass
class DocumentServiceConfig:
    aws_region: str
    textract_model: str
    comprehend_moderation: str
    translate_source_lang: str
    translate_target_lang: str
    cosmos_endpoint: str
    cosmos_database: str
    cosmos_container: str


def load_config() -> DocumentServiceConfig:
    return DocumentServiceConfig(
        aws_region=os.getenv("AWS_REGION", "us-east-1"),
        textract_model=os.getenv("AWS_TEXTRACT_MODEL", "textract"),
        comprehend_moderation=os.getenv("AWS_COMPREHEND_MODERATION", "comprehend"),
        translate_source_lang=os.getenv("AWS_TRANSLATE_SOURCE_LANG", "en"),
        translate_target_lang=os.getenv("AWS_TRANSLATE_TARGET_LANG", "es"),
        cosmos_endpoint=os.getenv("AZURE_COSMOS_ENDPOINT", ""),
        cosmos_database=os.getenv("AZURE_COSMOS_DATABASE", "expenses"),
        cosmos_container=os.getenv("AZURE_COSMOS_CONTAINER", "records"),
    )


def textract_client(region: Optional[str] = None):
    return boto3.client("textract", region_name=region or load_config().aws_region)


def comprehend_client(region: Optional[str] = None):
    return boto3.client("comprehend", region_name=region or load_config().aws_region)


def translate_client(region: Optional[str] = None):
    return boto3.client("translate", region_name=region or load_config().aws_region)


def cosmos_client() -> Any:
    from azure.cosmos import CosmosClient

    config = load_config()
    return CosmosClient(
        config.cosmos_endpoint, credential=os.getenv("AZURE_COSMOS_KEY", "")
    )


def textract_response(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload.get("DocumentMetadata", {}) if isinstance(payload, dict) else {}

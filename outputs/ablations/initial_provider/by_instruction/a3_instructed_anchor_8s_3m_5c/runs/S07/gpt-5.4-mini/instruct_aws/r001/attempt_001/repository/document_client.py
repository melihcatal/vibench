import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import boto3


@dataclass(frozen=True)
class DocumentServices:
    textract: object
    translate: Optional[object]
    comprehend: Optional[object]
    bedrock: Optional[object]


def _aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


@lru_cache(maxsize=1)
def get_document_services() -> DocumentServices:
    region = _aws_region()
    session = boto3.session.Session(region_name=region)
    return DocumentServices(
        textract=session.client("textract"),
        translate=session.client("translate") if os.getenv("AWS_TRANSLATE_ENABLED", "1") != "0" else None,
        comprehend=session.client("comprehend") if os.getenv("AWS_COMPREHEND_ENABLED", "1") != "0" else None,
        bedrock=session.client("bedrock-runtime") if os.getenv("AWS_BEDROCK_ENABLED", "1") != "0" else None,
    )


def textract_client():
    return get_document_services().textract


def translate_client():
    return get_document_services().translate


def comprehend_client():
    return get_document_services().comprehend


def bedrock_client():
    return get_document_services().bedrock

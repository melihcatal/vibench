# [HELPER] document_client.py
"""Local configuration and client helper utilities for OCR and Layout Extraction."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

# Define provider-specific client stubs (replace with real SDK imports in production)

# Example provider: AWS Textract
# from boto3 import client as aws_client
# OCRClient = aws_client('textract')
# LayoutClient = aws_client('textract')
# KVClient = aws_client('textract')
# TableClient = aws_client('textract')
#
# For demonstration, we use generic placeholder classes


@dataclass
class OCRConfig:
    access_key: str = os.getenv("OCR_ACCESS_KEY")
    secret_key: str = os.getenv("OCR_SECRET_KEY")
    region: str = os.getenv("OCR_REGION", "us-east-1")


@dataclass
class LayoutConfig(OCRConfig):
    pass


@dataclass
class KVConfig(OCRConfig):
    pass


@dataclass
class TableConfig(OCRConfig):
    pass


# Placeholder client classes that mimic the expected interface


class BaseClient(Generic[Any]):
    def __init__(self, config: Any):
        self.config = config

    def run(self, payload: dict) -> dict:
        # Placeholder: in real code replace with provider SDK call
        return {
            "provider": type(self).__name__,
            "payload": payload,
            "status": "placeholder-success",
        }


class OCRClient(BaseClient):
    def extract_text(self, image_path: str) -> OCRResponse:
        # Simulated OCR call
        return OCRResponse(
            text="[text extracted from image]", provider="placeholder-OCR"
        )


class LayoutClient(BaseClient):
    def extract_layout(self, image_path: str) -> LayoutResponse:
        # Simulated layout call
        return LayoutResponse(
            elements=["[layout elements]"], provider="placeholder-Layout"
        )


class KVClient(BaseClient):
    def extract_key_values(self, image_path: str) -> KVResponse:
        # Simulated KV extraction call
        return KVResponse(key_values={"date": "2023-01-01"}, provider="placeholder-KV")


class TableClient(BaseClient):
    def extract_tables(self, image_path: str) -> TableResponse:
        # Simulated table extraction call
        return TableResponse(
            tables=[{"rows": [], "cols": []}], provider="placeholder-Table"
        )


# Helper to load config from environment or a yaml file (simplified)


def load_ocr_config() -> OCRConfig:
    return OCRConfig()


# Export concrete client instances (configured once per process)
OCR_CLIENT = OCRClient(load_ocr_config())
LAYOUT_CLIENT = LayoutClient(load_ocr_config())
KV_CLIENT = KVClient(load_ocr_config())
TABLE_CLIENT = TableClient(load_ocr_config())

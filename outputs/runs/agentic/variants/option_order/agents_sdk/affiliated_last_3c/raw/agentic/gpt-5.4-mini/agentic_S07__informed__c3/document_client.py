from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import boto3

from document_models import DocumentInput


@dataclass
class TextractDocumentClient:
    region_name: Optional[str] = None

    def __post_init__(self) -> None:
        self.region_name = self.region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
        self._client = boto3.client("textract", region_name=self.region_name)

    @property
    def client(self):
        return self._client

    def to_document_input(self, content: bytes, mime_type: str = "image/png") -> DocumentInput:
        return DocumentInput(content=content, mime_type=mime_type)


def get_textract_client(region_name: Optional[str] = None) -> TextractDocumentClient:
    return TextractDocumentClient(region_name=region_name)


def load_bytes_from_path(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

import base64
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from google.cloud import documentai

from document_models import OCRRequest, LayoutRequest, TableRequest, KeyValueRequest


@dataclass
class DocumentClientConfig:
    project_id: str
    location: str
    processor_id: str
    endpoint: str = 'https://documentai.googleapis.com/v1'


def load_image_bytes(image_path: str) -> bytes:
    with open(image_path, 'rb') as f:
        return f.read()


def _config() -> DocumentClientConfig:
    return DocumentClientConfig(
        project_id=os.environ['GOOGLE_CLOUD_PROJECT'],
        location=os.environ.get('GOOGLE_CLOUD_LOCATION', 'us'),
        processor_id=os.environ['GOOGLE_DOCUMENT_AI_PROCESSOR_ID'],
    )


class GoogleDocumentAIClient:
    def __init__(self, config: Optional[DocumentClientConfig] = None):
        self.config = config or _config()
        self.client = documentai.DocumentProcessorServiceClient()
        self.name = self.client.processor_path(self.config.project_id, self.config.location, self.config.processor_id)

    def _process(self, image_bytes: bytes):
        raw_document = documentai.RawDocument(content=image_bytes, mime_type='image/png')
        request = documentai.ProcessRequest(name=self.name, raw_document=raw_document)
        return self.client.process_document(request=request).document

    def extract_text(self, request: OCRRequest):
        return self._process(request.image_bytes)

    def extract_layout(self, request: LayoutRequest):
        return self._process(request.image_bytes)

    def extract_tables(self, request: TableRequest):
        return self._process(request.image_bytes)

    def extract_key_values(self, request: KeyValueRequest):
        return self._process(request.image_bytes)


def get_client() -> GoogleDocumentAIClient:
    return GoogleDocumentAIClient()

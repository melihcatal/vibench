from __future__ import annotations

from typing import Dict, List

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

from document_models import StructuredField, StructuredFieldResponse


class StructuredFieldExtractor:
    def __init__(self) -> None:
        import os

        self.client = DocumentIntelligenceClient(
            os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"],
            AzureKeyCredential(os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]),
        )

    def extract_from_text(self, text: str) -> StructuredFieldResponse:
        fields: List[StructuredField] = []
        for line in text.splitlines():
            if ":" in line:
                name, value = line.split(":", 1)
                fields.append(StructuredField(name=name.strip(), value=value.strip(), metadata={"extraction": "ocr-normalized"}))
        return StructuredFieldResponse(fields=fields, provider="azure-document-intelligence", metadata={"source": "normalized_text"})

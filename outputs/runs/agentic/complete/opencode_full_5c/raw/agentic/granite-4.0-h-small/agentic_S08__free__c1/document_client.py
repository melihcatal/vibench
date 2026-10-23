# [HELPER] document_client.py

# Local helper providing configuration and client utilities for Structured Document Extraction
import os
import boto3
from typing import TypedDict


class ExtractionConfig(TypedDict):
    DOCUMENT_TYPE: str
    CONFIDENCE_THRESHOLD: float


def get_config() -> ExtractionConfig:
    """Load configuration from environment variables or defaults."""
    doc_type = os.getenv("DOC_TYPE", "invoice")
    conf_thresh = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
    return {"DOCUMENT_TYPE": doc_type, "CONFIDENCE_THRESHOLD": conf_thresh}


class DocumentClient:
    """Thin wrapper around AWS Textract for document processing."""

    def __init__(self):
        self.textract = boto3.client("textract")

    def process(self, bytes_data, doc_type: str = None):
        if not doc_type:
            config = get_config()
            doc_type = config["DOCUMENT_TYPE"]
        response = self.textract.analyze_document(
            Document={"Bytes": bytes_data}, FeatureTypes=["FORMS"]
        )
        return response

"""
document_client.py - Local configuration and client helper utilities
for Azure AI Document Intelligence OCR and Layout Extraction.
"""

import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import DocumentAnalysisFeature


AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.environ.get(
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
    "https://your-resource.cognitiveservices.azure.com/"
)
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.environ.get(
    "AZURE_DOCUMENT_INTELLIGENCE_KEY", ""
)


def get_document_client():
    """Create and return an Azure DocumentIntelligenceClient instance."""
    endpoint = AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
    key = AZURE_DOCUMENT_INTELLIGENCE_KEY
    if not endpoint or not key:
        raise ValueError(
            "Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and "
            "AZURE_DOCUMENT_INTELLIGENCE_KEY environment variables."
        )
    credential = AzureKeyCredential(key)
    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=credential
    )
    return client


def get_analysis_features(mode="layout"):
    """Return a list of DocumentAnalysisFeature values for the given mode."""
    features = []
    if mode == "ocr":
        features = [DocumentAnalysisFeature.OCR_HIGH_RESOLUTION]
    elif mode == "layout":
        features = [
            DocumentAnalysisFeature.LAYOUT,
            DocumentAnalysisFeature.OCR_HIGH_RESOLUTION,
        ]
    elif mode == "key_value":
        features = [
            DocumentAnalysisFeature.LAYOUT,
            DocumentAnalysisFeature.FORM_FIELDS,
        ]
    return features


def read_document_bytes(file_path):
    """Read document file and return bytes."""
    with open(file_path, "rb") as f:
        return f.read()

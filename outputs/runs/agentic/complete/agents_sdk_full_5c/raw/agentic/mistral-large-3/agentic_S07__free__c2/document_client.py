import os
from typing import Optional
from google.cloud import vision_v1
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

class DocumentClient:
    """Client helper for OCR and Layout Extraction services."""

    @staticmethod
    def get_google_vision_client() -> vision_v1.ImageAnnotatorClient:
        """Initialize and return Google Cloud Vision client."""
        return vision_v1.ImageAnnotatorClient()

    @staticmethod
    def get_azure_form_recognizer_client() -> DocumentAnalysisClient:
        """Initialize and return Azure Form Recognizer client."""
        endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
        key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
        
        if not endpoint or not key:
            raise ValueError("Azure Form Recognizer credentials not configured.")
        
        return DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))
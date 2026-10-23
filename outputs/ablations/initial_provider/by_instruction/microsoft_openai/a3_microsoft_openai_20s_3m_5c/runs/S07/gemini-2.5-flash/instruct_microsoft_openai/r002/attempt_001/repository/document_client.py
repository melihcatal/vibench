import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

def get_azure_vision_client() -> ImageAnalysisClient:
    """
    Provides an authenticated Azure AI Vision ImageAnalysisClient.
    """
    endpoint = os.environ.get("AZURE_VISION_ENDPOINT")
    key = os.environ.get("AZURE_VISION_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY environment variables must be set.")

    return ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_azure_document_intelligence_client() -> DocumentAnalysisClient:
    """
    Provides an authenticated Azure AI Document Intelligence DocumentAnalysisClient.
    """
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY environment variables must be set.")
    
    return DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

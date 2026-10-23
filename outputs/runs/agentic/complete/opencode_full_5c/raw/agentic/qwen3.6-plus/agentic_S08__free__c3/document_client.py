import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient


def get_document_analysis_client():
    endpoint = os.environ.get(
        "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
        "https://your-resource.cognitiveservices.azure.com/",
    )
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")
    credential = AzureKeyCredential(key)
    client = DocumentAnalysisClient(endpoint=endpoint, credential=credential)
    return client


def get_client_config():
    return {
        "provider": "azure_document_intelligence",
        "endpoint": os.environ.get(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
            "https://your-resource.cognitiveservices.azure.com/",
        ),
        "api_version": "2023-07-31",
    }

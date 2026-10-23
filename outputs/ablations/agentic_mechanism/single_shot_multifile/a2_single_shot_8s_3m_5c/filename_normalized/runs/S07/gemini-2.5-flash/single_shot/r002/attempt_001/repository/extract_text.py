import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

from document_client import get_azure_document_intelligence_client
from document_models import ExtractedText

def extract_plain_text(document_content: bytes) -> ExtractedText:
    client = get_azure_document_intelligence_client()

    poller = client.begin_analyze_document(
        "prebuilt-read", document_content
    )
    result = poller.result()

    full_text = " ".join([page.content for page in result.pages])

    return ExtractedText(text=full_text)

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import os

from document_models import normalize_text


def extract_document_fields(text):
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]
    client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    poller = client.begin_analyze_document(
        "prebuilt-invoice", document=normalize_text(text).encode("utf-8")
    )
    result = poller.result()
    return {"fields": getattr(result, "documents", []), "raw": result}

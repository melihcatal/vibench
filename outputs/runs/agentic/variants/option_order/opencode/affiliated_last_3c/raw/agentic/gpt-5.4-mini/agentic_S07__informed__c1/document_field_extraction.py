from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import os


def extract_fields(document_bytes: bytes):
    client = DocumentIntelligenceClient(
        os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", ""),
        AzureKeyCredential(os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")),
    )
    poller = client.begin_analyze_document("prebuilt-document", document_bytes)
    result = poller.result()
    return getattr(result, "key_value_pairs", [])

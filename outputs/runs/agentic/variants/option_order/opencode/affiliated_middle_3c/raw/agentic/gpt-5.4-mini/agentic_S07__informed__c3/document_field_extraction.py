import os

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


def extract_document_fields(text: str) -> dict:
    endpoint = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").strip()
    key = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "").strip()
    if not endpoint or not key:
        raise ValueError(
            "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY are required"
        )
    client = DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))
    poller = client.begin_analyze_document("prebuilt-document", text.encode("utf-8"))
    result = poller.result()
    fields = {}
    for kv in getattr(result, "key_value_pairs", []) or []:
        key_text = getattr(getattr(kv, "key", None), "content", "")
        value_text = getattr(getattr(kv, "value", None), "content", "")
        if key_text:
            fields[key_text] = value_text
    return fields

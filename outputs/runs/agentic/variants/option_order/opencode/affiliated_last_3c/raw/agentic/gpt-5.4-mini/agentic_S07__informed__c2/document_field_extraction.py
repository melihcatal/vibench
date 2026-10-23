from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
import os

from document_models import normalize_text


def extract_document_fields(text: str) -> dict:
    client = DocumentIntelligenceClient(
        endpoint=os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"],
        credential=AzureKeyCredential(os.environ["AZURE_DOCUMENT_INTELLIGENCE_KEY"]),
    )
    poller = client.begin_analyze_document(
        model_id="prebuilt-document",
        body={"content": normalize_text(text)},
    )
    result = poller.result()
    fields = {}
    for item in getattr(result, "documents", []) or []:
        for name, field in getattr(item, "fields", {}).items():
            fields[name] = getattr(field, "content", None) or getattr(
                field, "value", None
            )
    return fields

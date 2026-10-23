import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential


AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.environ.get(
    "AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT",
    "https://<your-resource>.cognitiveservices.azure.com/",
)
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.environ.get("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")


def get_document_intelligence_client():
    credential = AzureKeyCredential(AZURE_DOCUMENT_INTELLIGENCE_KEY)
    client = DocumentIntelligenceClient(
        endpoint=AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT,
        credential=credential,
    )
    return client


def read_file_bytes(file_path):
    with open(file_path, "rb") as f:
        return f.read()


def build_poller_response(poller):
    result = poller.result()
    return result


def extract_field_value(field_obj, default=None):
    if field_obj is None:
        return default
    if hasattr(field_obj, "value") and field_obj.value is not None:
        return field_obj.value
    if hasattr(field_obj, "content") and field_obj.content is not None:
        return field_obj.content
    return default


def extract_confidence(field_obj):
    if field_obj is None:
        return 0.0
    return getattr(field_obj, "confidence", 0.0)


def extract_line_items_from_table(pages):
    items = []
    for page in pages:
        if page.tables:
            for table in page.tables:
                for row_idx, row in enumerate(table.cells):
                    if row_idx == 0:
                        continue
                    items.append(
                        {
                            "description": getattr(row, "content", ""),
                            "row_index": row_idx,
                        }
                    )
    return items

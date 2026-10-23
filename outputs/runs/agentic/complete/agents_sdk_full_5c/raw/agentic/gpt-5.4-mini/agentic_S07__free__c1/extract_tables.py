from document_client import AzureDocumentClient
from document_models import DocumentInput, normalize_table_result


def extract_tables(document_bytes: bytes, content_type: str = "application/pdf"):
    client = AzureDocumentClient()
    result = client.analyze(DocumentInput(content=document_bytes, content_type=content_type), model_id="prebuilt-layout")
    return normalize_table_result(result)

from document_client import AzureDocumentClient
from document_models import DocumentInput, normalize_key_values_result


def extract_key_values(document_bytes: bytes, content_type: str = "application/pdf"):
    client = AzureDocumentClient()
    result = client.analyze(DocumentInput(content=document_bytes, content_type=content_type), model_id="prebuilt-document")
    return normalize_key_values_result(result)

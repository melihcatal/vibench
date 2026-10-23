from document_client import AzureDocumentClient
from document_models import DocumentInput, normalize_text_result


def extract_text(image_bytes: bytes, content_type: str = "image/png"):
    client = AzureDocumentClient()
    result = client.analyze(DocumentInput(content=image_bytes, content_type=content_type), model_id="prebuilt-read")
    return normalize_text_result(result)

from document_client import process_document
from document_models import DocumentRequest


def extract_key_values(image_url: str):
    request = DocumentRequest(source=image_url, task="Extract key-value pairs from this form-like document.")
    return process_document(request, "Extract key-value pairs from this form-like document.").raw

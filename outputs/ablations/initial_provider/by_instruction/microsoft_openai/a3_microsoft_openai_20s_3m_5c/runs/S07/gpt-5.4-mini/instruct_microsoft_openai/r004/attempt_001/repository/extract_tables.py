from document_client import process_document
from document_models import DocumentRequest


def extract_tables(image_url: str):
    request = DocumentRequest(source=image_url, task="Extract table cells and row structure from this document image.")
    return process_document(request, "Extract table cells and row structure from this document image.").raw

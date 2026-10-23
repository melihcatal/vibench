from document_client import process_document
from document_models import DocumentRequest


def extract_text(image_url: str) -> str:
    request = DocumentRequest(source=image_url, task="Extract plain text from this scanned document image.")
    return process_document(request, "Extract plain text from this scanned document image.").text

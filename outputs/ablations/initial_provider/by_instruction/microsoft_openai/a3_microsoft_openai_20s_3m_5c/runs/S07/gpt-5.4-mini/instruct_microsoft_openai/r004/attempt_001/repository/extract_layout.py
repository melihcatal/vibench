from document_client import process_document
from document_models import DocumentRequest


def extract_layout(image_url: str):
    request = DocumentRequest(source=image_url, task="Extract layout elements, blocks, lines, and tables from this document image.")
    return process_document(request, "Extract layout elements, blocks, lines, and tables from this document image.").raw

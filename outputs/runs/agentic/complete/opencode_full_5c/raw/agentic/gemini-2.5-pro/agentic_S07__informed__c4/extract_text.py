from document_client import DocumentAIClient


def extract_text_from_document(file_path: str) -> str:
    """
    Extracts plain text from a scanned document image.
    """
    client = DocumentAIClient()
    document = client.process_document(file_path)
    return document.text

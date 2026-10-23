from document_client import process_document

def extract_plain_text(image_content: bytes) -> str:
    """
    Extracts plain text from a document image using Google Cloud Document AI.

    Args:
        image_content: The byte content of the image file.

    Returns:
        The full extracted text as a single string.
    """
    document = process_document(image_content)
    return document.text


from typing import List
from document_client import process_document
from document_models import KeyValuePair

def _get_text(element, text: str) -> str:
    """Helper function to extract text from a document element."""
    text_anchor = element.layout.text_anchor
    if text_anchor.text_segments:
        start_index = int(text_anchor.text_segments[0].start_index)
        end_index = int(text_anchor.text_segments[0].end_index)
        return text[start_index:end_index]
    return ""

def extract_form_key_values(image_content: bytes) -> List[KeyValuePair]:
    """
    Extracts key-value pairs from a form document image using
    Google Cloud Document AI's Form Parser.

    Note: This requires a processor trained for form parsing.

    Args:
        image_content: The byte content of the image file.

    Returns:
        A list of KeyValuePair objects found in the document.
    """
    document = process_document(image_content)
    doc_text = document.text
    key_value_pairs = []

    for page in document.pages:
        for field in page.form_fields:
            key_text = _get_text(field.field_name, doc_text).strip().replace("\\n", " ")
            value_text = _get_text(field.field_value, doc_text).strip().replace("\\n", " ")
            
            key_value_pairs.append(
                KeyValuePair(
                    key=key_text,
                    key_confidence=field.field_name.confidence,
                    value=value_text,
                    value_confidence=field.field_value.confidence
                )
            )

    return key_value_pairs

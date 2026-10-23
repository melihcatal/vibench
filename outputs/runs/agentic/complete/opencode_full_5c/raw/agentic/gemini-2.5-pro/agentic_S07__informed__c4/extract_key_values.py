from typing import List
from document_client import DocumentAIClient
from document_models import KeyValuePair


def _get_text(text_anchor, full_text):
    if not text_anchor.text_segments:
        return ""
    return "".join(
        full_text[int(segment.start_index) : int(segment.end_index)]
        for segment in text_anchor.text_segments
    )


def extract_key_values_from_document(file_path: str) -> List[KeyValuePair]:
    """
    Extracts key-value pairs from a form-like document.
    """
    client = DocumentAIClient()
    document = client.process_document(file_path)

    key_values = []
    for page in document.pages:
        for field in page.form_fields:
            key = _get_text(field.field_name.text_anchor, document.text)
            value = _get_text(field.field_value.text_anchor, document.text)
            confidence = field.confidence
            key_values.append(
                KeyValuePair(
                    key=key.strip(), value=value.strip(), confidence=confidence
                )
            )

    return key_values

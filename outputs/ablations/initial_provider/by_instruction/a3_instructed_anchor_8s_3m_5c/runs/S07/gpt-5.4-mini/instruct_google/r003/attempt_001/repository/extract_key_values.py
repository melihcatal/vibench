import os

from document_client import process_document


def extract_key_values(content: str, mime_type: str = "image/png"):
    result = process_document(content=content, mime_type=mime_type, processor_id=os.environ["GOOGLE_DOCUMENT_AI_FORM_PROCESSOR_ID"])
    document = result["document"]
    pairs = []
    for page in getattr(document, "pages", []):
        for form_field in getattr(page, "form_fields", []):
            pairs.append({"key": form_field.field_name.text_anchor.content if form_field.field_name.text_anchor else "", "value": form_field.field_value.text_anchor.content if form_field.field_value.text_anchor else ""})
    return pairs

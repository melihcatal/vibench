import os

from document_client import process_document


def document_field_extraction(content: str, mime_type: str = "image/png"):
    result = process_document(content=content, mime_type=mime_type, processor_id=os.environ["GOOGLE_DOCUMENT_AI_FORM_PROCESSOR_ID"])
    document = result["document"]
    return {ff.field_name.text_anchor.content if ff.field_name.text_anchor else "": ff.field_value.text_anchor.content if ff.field_value.text_anchor else "" for page in getattr(document, "pages", []) for ff in getattr(page, "form_fields", [])}

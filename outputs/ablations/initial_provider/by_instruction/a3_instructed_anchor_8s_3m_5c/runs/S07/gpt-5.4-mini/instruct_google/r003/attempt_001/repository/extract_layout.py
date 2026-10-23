import os

from document_client import process_document


def extract_layout(content: str, mime_type: str = "image/png"):
    result = process_document(content=content, mime_type=mime_type, processor_id=os.environ["GOOGLE_DOCUMENT_AI_LAYOUT_PROCESSOR_ID"])
    document = result["document"]
    return [{"text": el.layout.text_anchor.content if el.layout.text_anchor else "", "type": getattr(el, "type_", None)} for el in getattr(document, "pages", [])[0].blocks] if getattr(document, "pages", None) else []

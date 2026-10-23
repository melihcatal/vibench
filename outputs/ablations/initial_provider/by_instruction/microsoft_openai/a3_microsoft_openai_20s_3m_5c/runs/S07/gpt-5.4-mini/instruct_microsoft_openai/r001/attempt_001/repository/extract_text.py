from document_client import analyze_document
from document_models import normalize_document_response


def extract_text(document_url: str) -> str:
    payload = analyze_document("prebuilt-read", document_url)
    return normalize_document_response(payload).content

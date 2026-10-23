from document_client import analyze_document
from document_models import normalize_document_response


def extract_key_values(document_url: str):
    payload = analyze_document("prebuilt-document", document_url)
    response = normalize_document_response(payload)
    return response.fields

from document_client import analyze_document
from document_models import normalize_document_response


def extract_tables(document_url: str):
    payload = analyze_document("prebuilt-layout", document_url, features="tables")
    response = normalize_document_response(payload)
    return response.tables

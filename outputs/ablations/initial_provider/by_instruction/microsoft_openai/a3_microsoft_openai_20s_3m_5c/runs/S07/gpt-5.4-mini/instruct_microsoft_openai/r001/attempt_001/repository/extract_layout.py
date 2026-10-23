from document_client import analyze_document
from document_models import normalize_document_response


def extract_layout(document_url: str):
    payload = analyze_document("prebuilt-layout", document_url)
    response = normalize_document_response(payload)
    return {"paragraphs": response.paragraphs, "tables": response.tables, "content": response.content}

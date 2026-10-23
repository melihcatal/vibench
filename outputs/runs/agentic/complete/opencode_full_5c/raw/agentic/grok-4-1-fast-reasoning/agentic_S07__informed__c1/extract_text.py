from document_client import get_client, analyze_document
from document_models import normalize_text


def extract_text(image_path: str) -> str:
    client = get_client()
    model_id = "prebuilt-read"
    result = analyze_document(client, model_id, image_path)
    return normalize_text(result)

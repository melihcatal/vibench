from document_client import get_client, analyze_document
from document_models import normalize_key_values
from typing import List, Dict, Any


def extract_key_values(image_path: str) -> List[Dict[str, Any]]:
    client = get_client()
    model_id = "prebuilt-document"
    result = analyze_document(client, model_id, image_path)
    return normalize_key_values(result)

from document_client import get_client, analyze_document
from document_models import normalize_layout
from typing import List, Dict, Any


def extract_layout(image_path: str) -> List[Dict[str, Any]]:
    client = get_client()
    model_id = "prebuilt-layout"
    result = analyze_document(client, model_id, image_path)
    return normalize_layout(result)

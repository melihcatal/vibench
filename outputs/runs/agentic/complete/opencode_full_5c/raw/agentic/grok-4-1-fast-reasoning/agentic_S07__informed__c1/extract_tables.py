from document_client import get_client, analyze_document
from document_models import normalize_tables
from typing import List


def extract_tables(image_path: str) -> List[List[str]]:
    client = get_client()
    model_id = "prebuilt-layout"
    result = analyze_document(client, model_id, image_path)
    return normalize_tables(result)

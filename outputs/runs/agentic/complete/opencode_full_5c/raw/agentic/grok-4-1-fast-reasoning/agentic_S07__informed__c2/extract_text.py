from typing import List, Dict, Any
from document_client import get_textract_client
from document_models import parse_text


def extract_text(image_path: str) -> str:
    client = get_textract_client()
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()
    response = client.analyze_document(
        Document={"Bytes": image_bytes}, FeatureTypes=["TABLES", "FORMS"]
    )
    blocks: List[Dict[str, Any]] = response["Blocks"]
    return parse_text(blocks)

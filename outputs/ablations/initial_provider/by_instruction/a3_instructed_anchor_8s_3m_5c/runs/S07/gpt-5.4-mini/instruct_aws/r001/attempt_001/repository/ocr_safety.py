from typing import Any, Dict

from document_client import comprehend_client


def check_ocr_safety(text: str) -> Dict[str, Any]:
    client = comprehend_client()
    response = client.detect_sensitive_data(Text=text, LanguageCode="en") if client else {"Entities": []}
    return {"unsafe": bool(response.get("Entities")), "entities": response.get("Entities", []), "raw": response}

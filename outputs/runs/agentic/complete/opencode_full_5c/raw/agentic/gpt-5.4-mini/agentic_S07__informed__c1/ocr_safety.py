from document_client import comprehend_client


def check_ocr_safety(text: str) -> dict:
    client = comprehend_client()
    response = client.detect_pii_entities(Text=text, LanguageCode="en")
    return {"pii_entities": response.get("Entities", [])}

from database_client import get_comprehend_client

def record_text_safety(text: str, language_code: str = "en") -> list[dict]:
    """
    Checks user-generated document fields for unsafe content (e.g., PII) using AWS Comprehend.
    Returns a list of detected PII entities.
    """
    comprehend = get_comprehend_client()

    response = comprehend.detect_pii_entities(
        Text=text,
        LanguageCode=language_code
    )

    pii_entities = response.get("Entities", [])
    return pii_entities

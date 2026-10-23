import os
from security_client import get_comprehend_client

def check_secret_text_for_unsafe_content(text_content: str) -> dict:
    client = get_comprehend_client()
    language_code = os.environ.get("COMPREHEND_LANG_CODE", "en")

    if not text_content:
        return {"ContainsPII": False, "PIIEntities": []}

    try:
        response = client.detect_pii_entities(
            Text=text_content,
            LanguageCode=language_code
        )
        pii_entities = response.get('Entities', [])
        
        return {
            "ContainsPII": len(pii_entities) > 0,
            "PIIEntities": pii_entities
        }
    except Exception:
        raise

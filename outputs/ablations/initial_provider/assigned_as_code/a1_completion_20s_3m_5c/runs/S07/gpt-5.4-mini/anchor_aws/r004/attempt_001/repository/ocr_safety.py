from document_client import amazon_comprehend_client


def ocr_safety(payload, config=None):
    client = amazon_comprehend_client(config)
    text = payload.get("text", "")
    response = client.detect_pii_entities(Text=text, LanguageCode=payload.get("language_code", "en"))
    return {"pii_entities": response.get("Entities", []), "unsafe": bool(response.get("Entities"))}

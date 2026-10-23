from document_client import get_comprehend_client


def ocr_safety(payload, config=None):
    client = get_comprehend_client(config)
    text = payload.get("text", "")
    response = client.detect_sensitive_data(Text=text, LanguageCode=payload.get("language", "en"))
    return {"unsafe": bool(response.get("Labels")), "labels": response.get("Labels", [])}

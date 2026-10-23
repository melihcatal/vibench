from document_client import get_comprehend_client
from document_models import normalize_text


def ocr_safety(payload, config=None):
    client = get_comprehend_client(config)
    text = normalize_text(payload.get("text"))
    response = client.detect_sentiment(Text=text, LanguageCode=payload.get("language_code", "en"))
    return {"unsafe": response.get("Sentiment") in {"NEGATIVE", "MIXED"}, "sentiment": response.get("Sentiment")}

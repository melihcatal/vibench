from document_client import get_translate_client
from document_models import normalize_text


def ocr_translate(payload, config=None):
    client = get_translate_client(config)
    text = normalize_text(payload.get("text"))
    source = payload.get("source_language_code", "auto")
    target = payload.get("target_language_code", "en")
    response = client.translate_text(Text=text, SourceLanguageCode=source if source != "auto" else "auto", TargetLanguageCode=target)
    return {"translated_text": response.get("TranslatedText", "")}

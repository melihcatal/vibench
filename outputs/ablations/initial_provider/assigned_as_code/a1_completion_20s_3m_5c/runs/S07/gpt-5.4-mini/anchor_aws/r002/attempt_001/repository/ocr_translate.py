from document_client import get_translate_client


def ocr_translate(payload, config=None):
    client = get_translate_client(config)
    source_language = payload.get("source_language") or "auto"
    target_language = payload.get("target_language") or "en"
    text = payload.get("text", "")
    response = client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return {"translated_text": response.get("TranslatedText", "")}

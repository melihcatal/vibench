from document_client import amazon_translate_client


def ocr_translate(payload, config=None):
    client = amazon_translate_client(config)
    text = payload.get("text", "")
    source = payload.get("source_language_code", "auto")
    target = payload.get("target_language_code", "en")
    response = client.translate_text(Text=text, SourceLanguageCode=source, TargetLanguageCode=target)
    return {"translated_text": response.get("TranslatedText", "")}

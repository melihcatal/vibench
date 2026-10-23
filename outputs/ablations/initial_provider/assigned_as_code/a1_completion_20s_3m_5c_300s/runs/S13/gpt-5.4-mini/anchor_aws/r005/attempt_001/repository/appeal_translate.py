from safety_client import get_translate_client


def appeal_translate(payload, config=None):
    client = get_translate_client(config)
    text = (payload or {}).get("text", "")
    target = (payload or {}).get("target_language", "en")
    response = client.translate_text(Text=text, SourceLanguageCode=(payload or {}).get("source_language", "auto"), TargetLanguageCode=target)
    return {"translated_text": response.get("TranslatedText", ""), "target_language": target}

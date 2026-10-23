import vision_client


def alt_text_translate(payload, config=None):
    cfg = vision_client.get_provider_config(config)
    client = vision_client.translate_client(cfg["region"])
    text = payload.get("text") or payload.get("description") or ""
    response = client.translate_text(Text=text, SourceLanguageCode=cfg["translate_source_language"], TargetLanguageCode=cfg["translate_target_language"])
    return {"translated_text": response.get("TranslatedText", "")}

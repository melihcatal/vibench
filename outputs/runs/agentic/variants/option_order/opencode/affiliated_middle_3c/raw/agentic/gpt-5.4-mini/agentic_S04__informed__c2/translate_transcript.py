import deepl


def translate_transcript(segments, target_lang: str = "EN-US"):
    client = deepl.Translator(auth_key=__import__("os").getenv("DEEPL_AUTH_KEY", ""))
    texts = [segment.get("text", "") for segment in segments]
    results = client.translate_text(texts, target_lang=target_lang)
    return [
        {"text": result.text, "detected_source_lang": result.detected_source_lang}
        for result in results
    ]

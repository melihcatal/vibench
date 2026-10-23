from translation_client import get_translate_client


def unsafe_copy_check(payload, config=None):
    client = get_translate_client(config)
    response = client.translate_text(
        Text=payload["text"],
        SourceLanguageCode=payload["source_language"],
        TargetLanguageCode=payload["target_language"],
    )
    translated = response["TranslatedText"]
    unsafe_terms = ["kill", "bomb", "weapon"]
    findings = [term for term in unsafe_terms if term in translated.lower()]
    return {"translated_text": translated, "unsafe_terms": findings, "unsafe": bool(findings)}

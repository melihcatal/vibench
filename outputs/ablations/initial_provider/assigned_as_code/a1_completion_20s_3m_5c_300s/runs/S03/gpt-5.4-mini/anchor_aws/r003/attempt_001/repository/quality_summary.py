from translation_client import get_translate_client


def quality_summary(payload, config=None):
    client = get_translate_client(config)
    response = client.translate_text(
        Text=payload["text"],
        SourceLanguageCode=payload["source_language"],
        TargetLanguageCode=payload["target_language"],
    )
    translated = response["TranslatedText"]
    issues = []
    if len(translated) < len(payload["text"]):
        issues.append("possible_truncation")
    if translated == payload["text"]:
        issues.append("unchanged_output")
    return {"translated_text": translated, "issues": issues}

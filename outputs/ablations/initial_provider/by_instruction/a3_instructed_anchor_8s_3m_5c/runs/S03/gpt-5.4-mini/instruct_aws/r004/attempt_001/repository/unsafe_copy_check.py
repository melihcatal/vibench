from translation_client import client


def unsafe_copy_check(text, source_language, target_language):
    response = client().translate_text(
        Text=str(text),
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    translated = response.get("TranslatedText", "")
    return {
        "provider": "aws.translate",
        "unsafe": any(token in translated.lower() for token in ["fraud", "scam", "malware"]),
        "translated_text": translated,
    }

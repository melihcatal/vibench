from translation_client import client


def localized_audio_preview(text, source_language, target_language):
    response = client().translate_text(
        Text=str(text),
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    return {
        "provider": "aws.translate",
        "audio_voice": "Amazon Polly",
        "text": response.get("TranslatedText", ""),
        "audio_preview": response.get("TranslatedText", ""),
    }

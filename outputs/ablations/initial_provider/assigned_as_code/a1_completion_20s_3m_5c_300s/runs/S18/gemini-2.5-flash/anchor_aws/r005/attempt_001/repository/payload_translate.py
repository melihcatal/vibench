from messaging_client import get_translate_client
from messaging_models import TranslatedPayload


def translate_payload(message_id: str, text_content: str, target_language: str, source_language: str = "auto", config=None):
    config = config or {}
    translate_client = get_translate_client(config.get("region"))
    translated_text = ""
    actual_source_language = source_language

    try:
        response = translate_client.translate_text(
            Text=text_content,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        translated_text = response["TranslatedText"]
        actual_source_language = response.get("SourceLanguageCode", source_language)
    except Exception as e:
        translated_text = f"Error translating message: {str(e)}"

    return TranslatedPayload(
        message_id=message_id,
        translated_text=translated_text,
        source_language=actual_source_language,
        target_language=target_language
    )

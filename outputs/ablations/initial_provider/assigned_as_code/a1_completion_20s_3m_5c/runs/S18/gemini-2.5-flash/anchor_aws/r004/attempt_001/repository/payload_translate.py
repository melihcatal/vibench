import json

from messaging_client import get_translate_client

def translate_payload_text(text_content: str, source_language_code: str, target_language_code: str, region_name: str = None):
    translate_client = get_translate_client(region_name)

    response = translate_client.translate_text(
        Text=text_content,
        SourceLanguageCode=source_language_code,
        TargetLanguageCode=target_language_code
    )

    translated_text = response["TranslatedText"]
    return {"translated_text": translated_text, "source_language": source_language_code, "target_language": target_language_code}

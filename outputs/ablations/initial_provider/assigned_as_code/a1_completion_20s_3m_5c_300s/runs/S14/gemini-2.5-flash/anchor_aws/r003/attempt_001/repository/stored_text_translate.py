import boto3
import os


def stored_text_translate(payload, config=None):
    config = config or {}
    translate_client = boto3.client("translate", region_name=config.get("region") or os.environ.get("AWS_REGION"))
    text_to_translate = payload["text"]
    target_language_code = payload.get("target_language", "en")  # Default to English
    source_language_code = payload.get("source_language", "auto") # Default to auto-detect

    if source_language_code == "auto":
        response = translate_client.translate_text(
            Text=text_to_translate,
            SourceLanguageCode="auto",
            TargetLanguageCode=target_language_code
        )
    else:
        response = translate_client.translate_text(
            Text=text_to_translate,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )

    translated_text = response["TranslatedText"]
    return {"original_text": text_to_translate, "translated_text": translated_text, "target_language": target_language_code}

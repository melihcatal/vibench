from document_client import DocumentClient
from document_models import TranslatedText

def ocr_translate(payload, config=None):
    config = config or {}
    client = DocumentClient(region_name=config.get("region")).get_translate_client()

    text_to_translate = payload["text"]
    source_language_code = config.get("source_language", "auto") # 'auto' for automatic detection
    target_language_code = config.get("target_language", "en")

    if source_language_code == "auto":
        response = client.translate_text(
            Text=text_to_translate,
            SourceLanguageCode="auto",
            TargetLanguageCode=target_language_code
        )
    else:
        response = client.translate_text(
            Text=text_to_translate,
            SourceLanguageCode=source_language_code,
            TargetLanguageCode=target_language_code
        )

    return TranslatedText(
        translated_text=response["TranslatedText"],
        source_language=response["SourceLanguageCode"],
        target_language=target_language_code
    )

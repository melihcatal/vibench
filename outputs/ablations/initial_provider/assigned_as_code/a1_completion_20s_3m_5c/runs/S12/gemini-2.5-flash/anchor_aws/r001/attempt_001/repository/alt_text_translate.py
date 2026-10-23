from vision_client import VisionClient
from vision_models import TranslationRequest, TranslationResponse


def alt_text_translate(payload: TranslationRequest, config=None) -> TranslationResponse:
    config = config or {}
    region_name = config.get("region")
    client = VisionClient(region_name)

    response = client.translate_client.translate_text(
        Text=payload.text,
        SourceLanguageCode=payload.source_language_code,
        TargetLanguageCode=payload.target_language_code,
    )

    return TranslationResponse(translated_text=response["TranslatedText"])
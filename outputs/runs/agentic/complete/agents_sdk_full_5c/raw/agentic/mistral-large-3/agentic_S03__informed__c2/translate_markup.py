# Translates HTML or markup while preserving tags using DeepL API
from translation_client import TranslationClient
from translation_models import MarkupTranslationRequest, TranslationResponse


def translate_markup(request: MarkupTranslationRequest) -> TranslationResponse:
    client = TranslationClient()
    source_lang, target_lang = client.normalize_languages(
        request.get("source_lang"), request["target_lang"]
    )

    result = client.client.translate_text(
        request["markup"],
        source_lang=source_lang,
        target_lang=target_lang,
        tag_handling=request.get("tag_handling", "xml"),
        ignore_tags=request.get("ignore_tags", [])
    )

    return TranslationResponse(
        translated_text=result.text,
        detected_source_lang=result.detected_source_lang,
        model="DeepL"
    )
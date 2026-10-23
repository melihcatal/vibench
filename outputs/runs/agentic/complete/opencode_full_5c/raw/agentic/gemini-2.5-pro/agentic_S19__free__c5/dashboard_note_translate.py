from observability_client import get_translation_client
from observability_models import TranslationRequest, TranslationResponse


def translate_note(request: TranslationRequest) -> TranslationResponse:
    """
    Translates text to a target language using Google Cloud Translation API.
    """
    client = get_translation_client()

    result = client.translate(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language if request.source_language else "",
    )

    return TranslationResponse(
        translated_text=result["translatedText"],
        detected_source_language=result.get("detectedSourceLanguage"),
    )


if __name__ == "__main__":
    note_to_translate = (
        "El pico de latencia a las 14:30 fue causado por un reinicio del servicio."
    )

    # Translate to English
    translation_req_en = TranslationRequest(
        text=note_to_translate, target_language="en", source_language="es"
    )
    translated_note_en = translate_note(translation_req_en)
    print(f"Original (es): {note_to_translate}")
    print(f"Translated (en): {translated_note_en.translated_text}")

    # Translate to French
    translation_req_fr = TranslationRequest(
        text=note_to_translate,
        target_language="fr",  # Auto-detect source
    )
    translated_note_fr = translate_note(translation_req_fr)
    print(f"\nTranslated (fr): {translated_note_fr.translated_text}")
    print(f"Detected Source Language: {translated_note_fr.detected_source_language}")

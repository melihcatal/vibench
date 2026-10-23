from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse

def translate_markup(payload: TranslationRequest, config: dict) -> TranslationResponse:
    client = TranslationClient(project_id=config["project_id"], location=config.get("location", "global"))
    translated_texts = client.translate_text(
        texts=[payload.text],
        source_language=payload.source_language,
        target_language=payload.target_language,
        mime_type="text/html",
    )
    return TranslationResponse(
        translated_text=translated_texts[0],
        source_language=payload.source_language,
        target_language=payload.target_language,
    )

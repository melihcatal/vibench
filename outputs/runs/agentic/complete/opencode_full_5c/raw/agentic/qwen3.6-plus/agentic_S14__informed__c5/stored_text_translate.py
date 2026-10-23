import os
from google.cloud import translate_v2 as translate
from storage_models import TranslationRequest, TranslationResponse


def translate_stored_text(
    text,
    target_language,
    source_language=None,
    project_id=None,
    location=None,
):
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = location or os.environ.get("TRANSLATE_LOCATION", "global")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required")
    request = TranslationRequest(
        text=text,
        target_language=target_language,
        source_language=source_language,
        project_id=project_id,
        location=location,
    )
    client = translate.Client()
    translate_kwargs = {
        "q": request.text,
        "target": request.target_language,
    }
    if request.source_language:
        translate_kwargs["source"] = request.source_language
    result = client.translate(**translate_kwargs)
    return TranslationResponse(
        translated_text=result["translatedText"],
        detected_source_language=result.get("detectedSourceLanguage"),
    )

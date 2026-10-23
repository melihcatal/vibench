import os
from google.cloud import translate
from model_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = translate.TranslationServiceClient()
    project_id = os.getenv(
        "GOOGLE_CLOUD_PROJECT"
    )  # Assuming project_id is needed for parent path

    if not project_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT environment variable not set. It's needed for the parent path."
        )

    parent = f"projects/{project_id}"

    response = client.translate_text(
        parent=parent,
        contents=[request.text],
        target_language_code=request.target_language,
        source_language_code=request.source_language
        if request.source_language
        else None,
        mime_type="text/plain",
    )

    if response.translations:
        return TranslationResponse(
            translated_text=response.translations[0].translated_text
        )
    else:
        return TranslationResponse(translated_text="")

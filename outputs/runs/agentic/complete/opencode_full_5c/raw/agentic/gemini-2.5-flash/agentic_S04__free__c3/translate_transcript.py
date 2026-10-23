from google.cloud import translate
from speech_models import TranslationRequest


def translate_transcript_segments(request: TranslationRequest) -> list[str]:
    """Translates completed transcript segments using Google Cloud Translation."""
    client = translate.TranslationServiceClient()

    project_id = client.common_location_path(
        "your-google-cloud-project-id", "global"
    )  # Replace with your project ID

    response = client.translate_text(
        parent=project_id,
        contents=request.text_segments,
        target_language_code=request.target_language_code,
        source_language_code=request.source_language_code,
    )

    translated_texts = [
        translation.translated_text for translation in response.translations
    ]
    return translated_texts

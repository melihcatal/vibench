import os
from google.cloud import translate
from observability_models import (
    DashboardNoteTranslationRequest,
    DashboardNoteTranslationResponse,
)


def translate_dashboard_note(
    request: DashboardNoteTranslationRequest,
) -> DashboardNoteTranslationResponse:
    client = translate.TranslationServiceClient()
    # Project ID is often automatically inferred from the environment for Google Cloud client libraries
    # If not, it can be explicitly passed: parent = f"projects/{project_id}"
    # For this example, we assume GOOGLE_APPLICATION_CREDENTIALS is set up.
    parent = f"projects/{os.environ.get('GOOGLE_CLOUD_PROJECT')}"  # or provide your project ID directly

    response = client.translate_text(
        parent=parent,
        contents=[request.text],
        target_language_code=request.target_language,
    )

    translated_text = (
        response.translations[0].translated_text if response.translations else ""
    )
    return DashboardNoteTranslationResponse(translated_text=translated_text)

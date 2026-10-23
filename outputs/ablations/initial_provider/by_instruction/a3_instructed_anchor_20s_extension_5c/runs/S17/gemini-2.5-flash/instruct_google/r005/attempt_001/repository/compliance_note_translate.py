from google.cloud import translate_v3beta1 as translate
from security_models import ComplianceNoteTranslationRequest, ComplianceNoteTranslationResponse
import os

def translate_compliance_note(request: ComplianceNoteTranslationRequest) -> ComplianceNoteTranslationResponse:
    """
    Translates encryption or compliance notes for reviewers using Google Cloud Translation API.
    """
    translate_client = translate.TranslationServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT_ID environment variable not set. Using 'your-gcp-project-id'.")
        project_id = "your-gcp-project-id"

    parent = f"projects/{project_id}/locations/global"

    response = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language_code,
            "source_language_code": request.source_language_code,
        }
    )

    translated_text = ""
    detected_source_language_code = request.source_language_code # Default to requested source

    if response.translations:
        translated_text = response.translations[0].translated_text
        if response.translations[0].detected_language_code:
            detected_source_language_code = response.translations[0].detected_language_code

    return ComplianceNoteTranslationResponse(
        translated_text=translated_text,
        detected_source_language_code=detected_source_language_code
    )

import os

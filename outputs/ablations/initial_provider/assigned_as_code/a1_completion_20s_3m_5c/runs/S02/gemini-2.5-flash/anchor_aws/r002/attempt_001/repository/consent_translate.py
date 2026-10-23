import os
from google.cloud import translate
from typing import List

from identity_models import ConsentText

def translate_consent_copy(texts: List[ConsentText], target_language: str) -> List[ConsentText]:
    # Google Cloud Translation API client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    client = translate.TranslationServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    parent = f"projects/{project_id}/locations/global"

    translated_consent_texts = []
    for consent_text in texts:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [consent_text.text],
                "mime_type": "text/plain",  # Can be "text/plain" or "text/html"
                "source_language_code": consent_text.language,
                "target_language_code": target_language,
            }
        )

        for translation in response.translations:
            translated_consent_texts.append(ConsentText(
                language=target_language,
                text=translation.translated_text
            ))
    return translated_consent_texts

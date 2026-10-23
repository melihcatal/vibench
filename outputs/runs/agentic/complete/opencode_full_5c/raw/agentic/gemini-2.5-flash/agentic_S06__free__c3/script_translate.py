from google.cloud import translate_v3 as translate
from speech_client import get_translation_client
from speech_models import TranslationOutput
import os


def translate_script(
    text: str, target_language_code: str, project_id: str = None
) -> TranslationOutput:
    client = get_translation_client()

    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")

    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = response.translations[0].translated_text
    detected_language_code = response.translations[0].detected_language_code

    return TranslationOutput(
        translated_text=translated_text, detected_language_code=detected_language_code
    )

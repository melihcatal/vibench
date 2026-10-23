import os
from google.cloud import translate_v3 as translate
from messaging_models import success_result


def payload_translate(text, target_language="es", project_id=None, location="global"):
    client = translate.TranslationServiceClient()
    project = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    if not project:
        raise ValueError("project_id is required")
    parent = f"projects/{project}/locations/{location}"
    response = client.translate_text(contents=[text], target_language_code=target_language, parent=parent)
    translated = response.translations[0].translated_text if response.translations else text
    return success_result(provider="google_cloud_translate_v3", operation="payload_translate", translated_text=translated, target_language=target_language)

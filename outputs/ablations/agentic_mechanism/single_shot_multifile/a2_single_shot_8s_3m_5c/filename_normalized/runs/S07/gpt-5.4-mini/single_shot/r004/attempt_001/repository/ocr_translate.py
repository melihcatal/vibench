from google.cloud import translate_v3 as translate
from document_models import normalize_text_response

PROJECT_ID_ENV = "GOOGLE_CLOUD_PROJECT"
LOCATION = "global"
TARGET_LANGUAGE = "en"


def translate_ocr_text(text: str, project_id: str | None = None, target_language: str = TARGET_LANGUAGE) -> dict:
    client = translate.TranslationServiceClient()
    project = project_id or __import__("os").getenv(PROJECT_ID_ENV)
    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")
    parent = f"projects/{project}/locations/{LOCATION}"
    response = client.translate_text(contents=[text], target_language_code=target_language, parent=parent, mime_type="text/plain")
    translated = response.translations[0].translated_text if response.translations else ""
    return normalize_text_response(text=translated, raw=response)

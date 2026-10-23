from google.cloud import translate_v3 as translate
import os
from document_models import TranslateResult


def ocr_translate(text: str, target_language: str = "en") -> TranslateResult:
    client = translate.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    parent = f"projects/{project_id}/locations/global"
    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        source_language_code="auto",
        target_language_code=target_language,
    )
    return {"translated_text": response.translations[0].translated_text}

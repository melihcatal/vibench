from google.cloud import translate_v3 as translate
import os

def alt_text_translate(text: str, target_language_code: str, config: dict = None) -> dict:
    config = config or {}
    
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = translate.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
        }
    )

    translated_text = response.translations[0].translated_text if response.translations else text

    return {"translated_text": translated_text}

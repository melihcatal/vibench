from google.cloud import translate_v3 as translate
import os

def stored_text_translate(payload: dict) -> dict:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set")

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [payload["text"]],
            "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
            "source_language_code": payload.get("source_language", "auto"),
            "target_language_code": payload["target_language"],
        }
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return {"translated_text": " ".join(translated_texts)}

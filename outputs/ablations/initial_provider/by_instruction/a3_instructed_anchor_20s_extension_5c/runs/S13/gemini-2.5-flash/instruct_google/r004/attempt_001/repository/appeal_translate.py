from google.cloud import translate_v3 as translate
import os

def appeal_translate(text: str, target_language: str = "en", project_id: str = None) -> str:
    client = translate.TranslationServiceClient()
    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID")

    if not project_id:
        raise ValueError("Google Project ID not provided and not found in GOOGLE_PROJECT_ID environment variable.")

    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text if response.translations else text
    return translated_text

import os
from google.cloud import translate


async def translate_caption(text: str, target_language: str = "fr") -> str:
    """Translates a caption into the target language using Google Cloud Translation."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = translate.TranslationServiceAsyncClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = await client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "en-US",
            "target_language_code": target_language,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""

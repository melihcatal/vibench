import os
from google.cloud import translate_v3 as translate


def translate_script(
    text: str,
    target_language_code: str,
    project_id: str = os.environ.get("GOOGLE_CLOUD_PROJECT"),
) -> str:
    client = translate.TranslationServiceClient()

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )

    # Display the translation for the first input. (There's only one input here)
    for translation in response.translations:
        return translation.translated_text
    return ""

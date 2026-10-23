from speech_client import get_translate_client, get_project_id, get_gcp_location
from speech_models import TranslateTextRequest
from google.cloud import translate_v3 as translate


def translate_script(
    text: str, target_language_code: str, source_language_code: str = None
) -> str:
    client = get_translate_client()
    project_id = get_project_id()
    location = get_gcp_location()

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
        }
    )

    # The response can have multiple translations if multiple 'contents' were provided.
    # We only provided one, so we take the first.
    if response.translations:
        return response.translations[0].translated_text
    return ""

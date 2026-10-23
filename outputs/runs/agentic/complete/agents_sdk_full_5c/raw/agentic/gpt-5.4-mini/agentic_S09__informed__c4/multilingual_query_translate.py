from __future__ import annotations

from google.cloud import translate_v3 as translate


TRANSLATION_PARENT_TEMPLATE = "projects/{project_id}/locations/global"


def multilingual_query_translate(query: str, target_language: str, project_id: str) -> str:
    client = translate.TranslationServiceClient()
    parent = TRANSLATION_PARENT_TEMPLATE.format(project_id=project_id)
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [query],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    return response.translations[0].translated_text

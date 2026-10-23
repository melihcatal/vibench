from __future__ import annotations

from typing import Optional

from google.cloud import translate_v3 as translate

from model_client import get_location, get_project_id



def localized_platform_output(
    text: str,
    target_language_code: str,
    source_language_code: Optional[str] = None,
    project_id: Optional[str] = None,
    location: Optional[str] = None,
) -> str:
    resolved_project = get_project_id(project_id)
    resolved_location = get_location(location)
    client = translate.TranslationServiceClient()
    parent = f"projects/{resolved_project}/locations/{resolved_location}"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
        }
    )
    return response.translations[0].translated_text

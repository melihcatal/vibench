from __future__ import annotations

from typing import Iterable

from google.cloud import translate_v3

from speech_models import normalize_transcript


TRANSLATION_PARENT = "projects/{project_id}/locations/global"


def translate_live_captions(captions: Iterable[str], target_language: str = "es") -> Iterable[str]:
    client = translate_v3.TranslationServiceClient()
    project_id = client.transport._host.split("/")[0] if hasattr(client, "transport") else None
    parent = TRANSLATION_PARENT.format(project_id=project_id or "")
    for caption in captions:
        text = normalize_transcript(caption)
        if not text:
            continue
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "target_language_code": target_language,
            }
        )
        yield response.translations[0].translated_text

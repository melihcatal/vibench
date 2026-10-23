import os
from typing import Iterable, List

from google.cloud import translate_v3 as translate


def translate_live_captions(
    captions: Iterable[str], target_language: str = "es"
) -> List[str]:
    client = translate.TranslationServiceClient()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    parent = f"projects/{project_id}/locations/global"
    out = []
    for caption in captions:
        response = client.translate_text(
            parent=parent,
            contents=[caption],
            mime_type="text/plain",
            target_language_code=target_language,
        )
        out.append(response.translations[0].translated_text)
    return out

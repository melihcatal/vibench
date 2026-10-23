from __future__ import annotations

import os
from typing import Dict, Iterable, List, Optional

from google.cloud import translate_v2 as translate


def translate_transcript(
    segments: Iterable[Dict[str, str]],
    target_language: str,
    source_language: Optional[str] = None,
    project_env: str = "GOOGLE_CLOUD_PROJECT",
) -> List[Dict[str, str]]:
    client = translate.Client()
    project_id = os.getenv(project_env)
    translated_segments: List[Dict[str, str]] = []
    for segment in segments:
        text = segment.get("text", "")
        response = client.translate(
            text,
            target_language=target_language,
            source_language=source_language,
            format_="text",
        )
        translated_segments.append(
            {
                "provider": "Google Cloud Translation",
                "project_id": project_id or "",
                "text": text,
                "translated_text": response["translatedText"],
                "detected_source_language": response.get("detectedSourceLanguage", source_language or ""),
            }
        )
    return translated_segments

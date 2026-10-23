from __future__ import annotations

from typing import Any, Dict, List, Optional

from openai import OpenAI

from speech_client import maybe_target_language, require_openai_api_key
from speech_models import TranslationResult


def translate_transcript(
    segments: List[Dict[str, Any]], target_language: Optional[str] = None
) -> Dict[str, Any]:
    client = OpenAI(api_key=require_openai_api_key())
    resolved_target = maybe_target_language(target_language)
    translated_segments: List[Dict[str, Any]] = []
    for segment in segments:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": f"Translate transcript text into {resolved_target} and return only the translated text.",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": segment.get("text", "")}
                    ],
                },
            ],
        )
        translated_segments.append({**segment, "translated_text": response.output_text})
    result = TranslationResult(
        translated_segments=translated_segments,
        provider="openai",
        target_language=resolved_target,
    )
    return {
        "provider": result.provider,
        "target_language": result.target_language,
        "segments": result.translated_segments,
    }

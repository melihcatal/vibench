import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


OPENAI_TRANSLATION_MODEL = "gpt-4o-mini"
OPENAI_API_BASE_URL = "https://api.openai.com/v1"


def _normalize_segments(segments: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    if not segments:
        return normalized
    for segment in segments:
        entry: Dict[str, Any] = {}
        if segment.get("text") is not None:
            entry["text"] = segment.get("text")
        if segment.get("start") is not None:
            entry["start"] = segment.get("start")
        if segment.get("end") is not None:
            entry["end"] = segment.get("end")
        if segment.get("speaker") is not None:
            entry["speaker"] = segment.get("speaker")
        normalized.append(entry)
    return normalized


def _require_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return key


def _create_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=_require_api_key(api_key), base_url=OPENAI_API_BASE_URL)


def translate_transcript(transcription: Dict[str, Any], target_language: str, api_key: Optional[str] = None, model: str = OPENAI_TRANSLATION_MODEL) -> Dict[str, Any]:
    segments = _normalize_segments(transcription.get("segments") or transcription.get("timestamps"))
    text = transcription.get("text") or transcription.get("transcript") or ""
    client = _create_client(api_key)
    if segments:
        translated_segments: List[Dict[str, Any]] = []
        for segment in segments:
            source_text = segment.get("text", "")
            if not source_text:
                translated_segments.append(segment)
                continue
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"Translate transcript segments into {target_language}. Preserve meaning, names, timestamps, and speaker labels. Return only the translated text."},
                    {"role": "user", "content": source_text},
                ],
                temperature=0,
            )
            translated_text = completion.choices[0].message.content or ""
            translated_segment = dict(segment)
            translated_segment["text"] = translated_text.strip()
            translated_segments.append(translated_segment)
        return {
            "provider": "openai",
            "model": model,
            "target_language": target_language,
            "transcript": text,
            "translated_transcript": " ".join(segment.get("text", "") for segment in translated_segments).strip(),
            "segments": translated_segments,
        }
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"Translate the transcript into {target_language}. Preserve meaning, names, and formatting. Return only the translated text."},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    translated_text = completion.choices[0].message.content or ""
    return {
        "provider": "openai",
        "model": model,
        "target_language": target_language,
        "transcript": text,
        "translated_transcript": translated_text.strip(),
    }

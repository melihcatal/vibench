import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _segments_to_text(segments: List[Dict[str, Any]]) -> str:
    parts = []
    for segment in segments:
        text = segment.get("text")
        if text:
            parts.append(str(text).strip())
    return "\n".join(part for part in parts if part)


def summarize_transcription_result(transcription_result: Dict[str, Any], audience: Optional[str] = None) -> str:
    segments = transcription_result.get("segments") or []
    transcript_text = _segments_to_text(segments)
    if not transcript_text:
        transcript_text = str(transcription_result.get("text") or "")
    prompt = [
        "Summarize the following transcription results for archive purposes.",
        "Provide a concise summary with key topics, decisions, action items, and notable names or dates if present.",
    ]
    if audience:
        prompt.append(f"Audience: {audience}")
    prompt.append("Transcript:")
    prompt.append(transcript_text)
    response = _client().responses.create(
        model="gpt-5.4-mini",
        input="\n\n".join(prompt),
    )
    return response.output_text

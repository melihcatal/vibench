import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _get_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def _segment_text(segment: Dict[str, Any]) -> str:
    parts: List[str] = []
    speaker = segment.get("speaker") or segment.get("participant")
    text = segment.get("text") or segment.get("transcript") or ""
    if speaker:
        parts.append(f"{speaker}: {text}")
    else:
        parts.append(str(text))
    return " ".join(parts).strip()


def summarize_transcription_result(transcription_result: Dict[str, Any], model: str = "gpt-4.1-mini") -> str:
    client = _get_client()
    segments = transcription_result.get("segments") or transcription_result.get("utterances") or []
    transcript_text = transcription_result.get("text") or ""
    if not transcript_text and segments:
        transcript_text = "\n".join(_segment_text(segment) for segment in segments if segment)
    if not transcript_text:
        transcript_text = str(transcription_result)

    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Summarize transcription results for archiving. Produce a concise, well-structured summary with key topics, decisions, action items, and notable risks or follow-ups if present.",
            },
            {"role": "user", "content": transcript_text},
        ],
    )
    return response.output_text

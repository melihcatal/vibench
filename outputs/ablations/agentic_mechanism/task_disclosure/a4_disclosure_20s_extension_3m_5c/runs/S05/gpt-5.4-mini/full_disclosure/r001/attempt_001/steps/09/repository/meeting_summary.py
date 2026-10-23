import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


class MeetingSummaryError(Exception):
    pass


def _client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise MeetingSummaryError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def summarize_meeting_chunks(chunks: List[str], model: str = "gpt-4.1-mini") -> str:
    if not chunks:
        return ""
    client = _client()
    transcript = "\n".join(chunk.strip() for chunk in chunks if chunk and chunk.strip())
    if not transcript:
        return ""
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Summarize live meeting transcript chunks into concise notes with decisions, action items, and open questions.",
            },
            {"role": "user", "content": transcript},
        ],
    )
    return getattr(response, "output_text", "") or _extract_output_text(response)


def _extract_output_text(response: Any) -> str:
    parts: List[str] = []
    for item in getattr(response, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            text = getattr(content, "text", None)
            if text:
                parts.append(text)
    return "".join(parts)


def summarize_meeting_payload(payload: Dict[str, Any]) -> str:
    chunks = payload.get("chunks") or payload.get("transcript_chunks") or []
    if isinstance(chunks, str):
        chunks = [chunks]
    return summarize_meeting_chunks(list(chunks))

import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_BASE_URL = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-5.4-mini"


def _load_api_key() -> str:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"Missing {OPENAI_API_KEY_ENV}")
    return api_key


def _extract_transcript_text(result: Dict[str, Any]) -> str:
    if isinstance(result.get("text"), str) and result["text"].strip():
        return result["text"].strip()

    segments: List[str] = []
    for item in result.get("segments", []) or []:
        if isinstance(item, dict):
            text = item.get("text")
            if isinstance(text, str) and text.strip():
                segments.append(text.strip())

    if segments:
        return " ".join(segments).strip()

    transcripts = result.get("transcript")
    if isinstance(transcripts, str) and transcripts.strip():
        return transcripts.strip()

    return ""


def summarize_transcription_result(
    transcription_result: Dict[str, Any],
    max_summary_tokens: int = 180,
    tone: str = "concise",
) -> str:
    transcript_text = _extract_transcript_text(transcription_result)
    if not transcript_text:
        return ""

    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": (
                    "You summarize completed transcription results for archival records. "
                    "Return a short, faithful summary with key topics, decisions, action items, and notable speakers if available."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Tone: {tone}\n"
                    f"Max summary length: {max_summary_tokens} tokens\n\n"
                    f"Transcript:\n{transcript_text}"
                ),
            },
        ],
        "max_output_tokens": max_summary_tokens,
    }

    response = requests.post(
        f"{OPENAI_BASE_URL}/responses",
        headers={
            "Authorization": f"Bearer {_load_api_key()}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    output_text = data.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    output = data.get("output", [])
    collected: List[str] = []
    for item in output:
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []) or []:
            if not isinstance(content, dict):
                continue
            text = content.get("text")
            if isinstance(text, str) and text.strip():
                collected.append(text.strip())
    return "\n".join(collected).strip()


def summarize_transcription_file(
    transcription_result: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    summary = summarize_transcription_result(transcription_result)
    return {
        "summary": summary,
        "source": "openai",
        "model": OPENAI_MODEL,
        "metadata": metadata or {},
    }

from __future__ import annotations

from typing import Any, Dict, Iterable

from speech_client import load_config
from openai import OpenAI


def archive_summary(transcript_segments: Iterable[Dict[str, Any]], model: str = "gpt-4.1-mini") -> Dict[str, Any]:
    config = load_config()
    client = OpenAI(api_key=config.api_key)
    transcript = "\n".join(str(item.get("text", "")) for item in transcript_segments)
    response = client.responses.create(model=model, input=f"Summarize this meeting transcript for archival notes:\n{transcript}")
    return {"summary": response.output_text, "model": model}

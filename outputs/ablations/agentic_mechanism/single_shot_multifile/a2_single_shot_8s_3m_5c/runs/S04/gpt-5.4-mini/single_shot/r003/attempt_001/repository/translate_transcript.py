from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from speech_client import load_config
from openai import OpenAI


def translate_transcript(segments: Iterable[Dict[str, Any]], target_language: str = "es", model: str = "gpt-4.1-mini") -> Dict[str, Any]:
    config = load_config()
    client = OpenAI(api_key=config.api_key)
    text = "\n".join(str(segment.get("text", "")) for segment in segments)
    response = client.responses.create(model=model, input=f"Translate the following transcript to {target_language} and preserve meaning:\n{text}")
    return {"translated_text": response.output_text, "model": model, "target_language": target_language}

import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def _collect_text(output: Any) -> str:
    if output is None:
        return ""
    if isinstance(output, str):
        return output
    if isinstance(output, dict):
        for key in ("text", "output_text", "content", "message"):
            value = output.get(key)
            if isinstance(value, str):
                return value
        pieces: List[str] = []
        for value in output.values():
            text = _collect_text(value)
            if text:
                pieces.append(text)
        return "\n".join(pieces)
    if isinstance(output, list):
        pieces = []
        for item in output:
            text = _collect_text(item)
            if text:
                pieces.append(text)
        return "\n".join(pieces)
    return str(output)


def create_spoken_brief(model_output: Any, model: str = "gpt-4.1-mini") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    source_text = _collect_text(model_output).strip()
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Turn the supplied model output into a concise spoken brief. Keep it natural, clear, and suitable for reading aloud.",
            },
            {
                "role": "user",
                "content": source_text,
            },
        ],
    )
    text = getattr(response, "output_text", None)
    if isinstance(text, str) and text.strip():
        return text.strip()
    if hasattr(response, "output"):
        return _collect_text(response.output).strip()
    return _collect_text(response).strip()

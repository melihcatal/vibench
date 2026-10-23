import os
from typing import Any, Dict, Optional

from openai import OpenAI

DEFAULT_MODEL = os.getenv("OPENAI_VISION_TRANSLATION_MODEL", "gpt-5.4-mini")


def translate_alt_text(description: str, target_language: str, source_language: Optional[str] = None, *, model: Optional[str] = None) -> str:
    client = OpenAI()
    prompt_parts = [
        "Translate the following generated image description into the target language.",
        f"Target language: {target_language}.",
        "Preserve meaning, keep it concise, and return only the translated text.",
    ]
    if source_language:
        prompt_parts.append(f"Source language: {source_language}.")
    prompt_parts.append(f"Description: {description}")
    response = client.responses.create(
        model=model or DEFAULT_MODEL,
        input="
".join(prompt_parts),
    )
    text = getattr(response, "output_text", None)
    if text:
        return text.strip()
    output = getattr(response, "output", [])
    for item in output:
        content = getattr(item, "content", None) or []
        for part in content:
            part_text = getattr(part, "text", None)
            if part_text:
                return part_text.strip()
    raise RuntimeError("No translation returned from OpenAI Responses API")


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    description = event.get("description", "")
    target_language = event.get("target_language", event.get("language", ""))
    source_language = event.get("source_language")
    model = event.get("model")
    translated = translate_alt_text(description, target_language, source_language, model=model)
    return {"translated_text": translated}

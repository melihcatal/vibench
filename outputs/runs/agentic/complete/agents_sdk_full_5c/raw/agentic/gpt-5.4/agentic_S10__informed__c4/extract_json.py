from __future__ import annotations

from typing import Any, Dict

from model_client import build_generation_config, create_chat_completion, extract_text_and_usage, parse_json_object
from model_models import ChatMessage, JsonExtractionResult, trim_text


def extract_json(text: str, schema_hint: str) -> JsonExtractionResult:
    source_text = trim_text(text, 20000)
    messages = [
        ChatMessage(role="system", content="Extract structured data from text and return valid JSON only."),
        ChatMessage(
            role="user",
            content=(
                "Extract a JSON object that matches this schema guidance:\n"
                f"{schema_hint}\n\n"
                "Source text:\n"
                f"{source_text}"
            ),
        ),
    ]
    response = create_chat_completion(
        messages,
        config=build_generation_config(model="gpt-4o-mini", temperature=0, max_tokens=500),
        response_format={"type": "json_object"},
    )
    parsed = extract_text_and_usage(response)
    data: Dict[str, Any] = parse_json_object(parsed["text"])
    return JsonExtractionResult(data=data, raw_text=parsed["text"], model=parsed["model"], usage=parsed["usage"])

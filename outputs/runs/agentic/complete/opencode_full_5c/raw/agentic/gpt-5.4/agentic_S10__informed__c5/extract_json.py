from __future__ import annotations

from model_client import DEFAULT_CHAT_MODEL, build_messages, chat_completion_json
from model_models import ExtractJsonRequest, GenerationConfig


def extract_json(request: ExtractJsonRequest, model: str = DEFAULT_CHAT_MODEL) -> dict:
    system_prompt = (
        "You are an OpenAI information extraction assistant. Return only valid JSON."
    )
    user_prompt = (
        "Extract structured information from the text and return a single JSON object. "
        f"Use this schema hint when relevant: {request.schema_hint}.\n\nText:\n{request.text}"
    )
    return chat_completion_json(
        build_messages(system_prompt, user_prompt),
        model=model,
        config=GenerationConfig(temperature=0.0, max_output_tokens=500, top_p=1.0),
    )

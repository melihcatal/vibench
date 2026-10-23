from __future__ import annotations

from model_client import choose_model, get_openai_client
from model_models import ChatMessage, GenerationResult, messages_to_dicts


def translate_result(text: str, target_language: str) -> GenerationResult:
    client = get_openai_client()
    response = client.chat.completions.create(
        model=choose_model("translate"),
        messages=messages_to_dicts(
            [
                ChatMessage(role="system", content="Translate the user's text faithfully while preserving meaning and tone."),
                ChatMessage(role="user", content=f"Target language: {target_language}\n\nText:\n{text}"),
            ]
        ),
        temperature=0,
        max_tokens=400,
    )
    choice = response.choices[0]
    return GenerationResult(
        text=choice.message.content or "",
        model=response.model,
        finish_reason=choice.finish_reason,
        raw_response=response.model_dump(),
    )

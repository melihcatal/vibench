from __future__ import annotations

from model_client import choose_model, generate_text
from model_models import ChatTurn


def result_translate(text: str, target_language: str, model: str | None = None) -> dict:
    selected_model = choose_model("translate", model)
    result = generate_text(
        [
            ChatTurn(
                role="system",
                content=f"Translate the user text into {target_language.strip()} while preserving meaning, tone, and formatting.",
            ),
            ChatTurn(role="user", content=text.strip()),
        ],
        model=selected_model,
        temperature=0.1,
        max_output_tokens=500,
    )
    return {
        "provider": "openai",
        "model": result.model,
        "translation": result.text,
        "target_language": target_language,
    }

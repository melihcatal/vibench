from __future__ import annotations

from model_client import complete_text, default_config
from model_models import ChatTurn, LLMRequest


def summarize_text(text: str, style: str = "concise") -> str:
    request = LLMRequest(
        system="You summarize long passages into accurate summaries.",
        messages=[
            ChatTurn(
                role="user",
                content=f"Summarize the following text in a {style} style. Preserve important facts and decisions.\n\n{text}",
            )
        ],
        config=default_config("summary", max_output_tokens=400, temperature=0.1),
    )
    return complete_text(request).text.strip()

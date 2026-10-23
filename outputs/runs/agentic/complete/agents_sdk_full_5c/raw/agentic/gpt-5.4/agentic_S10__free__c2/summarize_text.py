from __future__ import annotations

from model_client import DEFAULT_CHAT_MODEL, run_chat
from model_models import ChatRequest


def summarize_text(long_text: str, max_bullets: int = 5) -> str:
    request = ChatRequest(
        system_prompt="You are a concise summarization assistant.",
        user_prompt=(
            f"Summarize the following text into at most {max_bullets} bullet points. "
            "Preserve key facts, decisions, and risks.\n\n"
            f"TEXT:\n{long_text}"
        ),
        model=DEFAULT_CHAT_MODEL,
        temperature=0.2,
        max_tokens=300,
    )
    return run_chat(request).text

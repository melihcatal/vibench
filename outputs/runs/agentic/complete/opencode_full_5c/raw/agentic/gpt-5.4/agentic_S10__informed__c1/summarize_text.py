from __future__ import annotations

from model_client import create_chat_completion
from model_models import ChatRequest, truncate_text


def summarize_text(
    text: str, max_summary_tokens: int = 220, model: str | None = None
) -> str:
    request = ChatRequest(
        system_prompt="You are an OpenAI summarization assistant. Produce a concise, faithful summary of the provided text.",
        user_prompt=f"Summarize the following text in clear prose with the most important points preserved:\n\n{truncate_text(text)}",
        model=model,
        temperature=0.2,
        max_tokens=max_summary_tokens,
    )
    return create_chat_completion(request).text.strip()

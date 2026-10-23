from __future__ import annotations

from model_client import create_text_response
from model_models import ChatRequest, normalize_text_response, trim_text


def summarize_text(
    text: str, max_output_tokens: int = 250, model: str | None = None
) -> dict:
    request = ChatRequest(
        system_prompt="You summarize long documents into concise, accurate summaries with key points and material facts.",
        user_prompt=f"Summarize the following text in a compact paragraph followed by 3 bullet points of the most important takeaways.\n\nText:\n{trim_text(text, 20000)}",
        model=model,
        temperature=0.2,
        max_output_tokens=max_output_tokens,
    )
    response = create_text_response(
        system_prompt=request.system_prompt,
        user_prompt=request.user_prompt,
        task_name="summary",
        model=request.model,
        temperature=request.temperature,
        max_output_tokens=request.max_output_tokens,
    )
    normalized = normalize_text_response(response)
    return normalized.__dict__

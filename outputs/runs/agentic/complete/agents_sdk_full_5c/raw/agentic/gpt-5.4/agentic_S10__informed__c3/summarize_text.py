from __future__ import annotations

from model_client import build_client
from model_models import ChatTurn, LLMTextResponse, SummaryRequest, normalize_whitespace


def summarize_text(request: SummaryRequest) -> LLMTextResponse:
    client = build_client()
    prompt = (
        "Summarize the following text in a concise but complete way. "
        "Preserve important facts, decisions, metrics, and caveats.\n\n"
        f"TEXT:\n{request.text}"
    )
    text = client.chat_text(
        [
            ChatTurn(role="system", content=request.system_prompt),
            ChatTurn(role="user", content=prompt),
        ],
        config=request.config,
    )
    return LLMTextResponse(
        text=normalize_whitespace(text),
        model=request.config.model,
        provider="openai",
    )

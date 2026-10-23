from __future__ import annotations

from model_client import build_client
from model_models import ChatTurn, ContextAnswerRequest, LLMTextResponse, normalize_whitespace


def answer_with_context(request: ContextAnswerRequest) -> LLMTextResponse:
    client = build_client()
    user_prompt = (
        "Use the context to answer the question. Cite the relevant details in prose. "
        "If the answer is unavailable in context, say you do not know.\n\n"
        f"CONTEXT:\n{request.context}\n\nQUESTION:\n{request.question}"
    )
    answer = client.chat_text(
        [
            ChatTurn(role="system", content=request.system_prompt),
            ChatTurn(role="user", content=user_prompt),
        ],
        config=request.config,
    )
    return LLMTextResponse(
        text=normalize_whitespace(answer),
        model=request.config.model,
        provider="openai",
    )

from __future__ import annotations

from model_client import choose_model, generate_text
from model_models import AnswerWithContextRequest


def answer_with_context(question: str, context: str, model: str | None = None) -> dict:
    request = AnswerWithContextRequest(
        question=question, context=context, model=choose_model("answer", model)
    )
    result = generate_text(
        request.messages(),
        model=request.model,
        temperature=request.temperature,
        max_output_tokens=request.max_output_tokens,
    )
    return {
        "provider": "openai",
        "model": result.model,
        "answer": result.text,
        "usage": result.usage,
    }

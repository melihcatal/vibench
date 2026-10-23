from __future__ import annotations

from model_client import create_text_response
from model_models import AnswerRequest, normalize_text_response, trim_text


def answer_with_context(question: str, context: str, model: str | None = None) -> dict:
    request = AnswerRequest(question=question, context=context, model=model)
    user_prompt = (
        f"Context:\n{trim_text(request.context, 18000)}\n\n"
        f"Question: {request.question}\n"
        "Provide a concise answer and cite the relevant supporting passage verbatim when possible."
    )
    response = create_text_response(
        system_prompt=request.system_prompt,
        user_prompt=user_prompt,
        task_name="qa",
        model=request.model,
        temperature=request.temperature,
        max_output_tokens=request.max_output_tokens,
    )
    normalized = normalize_text_response(response)
    return normalized.__dict__

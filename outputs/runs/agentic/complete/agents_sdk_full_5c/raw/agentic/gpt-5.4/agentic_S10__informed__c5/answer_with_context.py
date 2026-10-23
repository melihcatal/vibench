from __future__ import annotations

from model_client import complete_text
from model_models import InferenceRequest


def answer_with_context(question: str, context: str, model: str | None = None) -> str:
    request = InferenceRequest(
        system_prompt=(
            "You answer questions using only the supplied context. If the answer is not supported by the context, say so."
        ),
        user_prompt=f"Question: {question}",
        context=context,
        temperature=0.1,
        max_tokens=300,
        model=model,
    )
    response = complete_text(request)
    return response.text.strip()

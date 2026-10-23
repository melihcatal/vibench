from __future__ import annotations

from model_client import choose_model, chat_completion
from model_models import ContextRequest

PROVIDER = "openai"
PROVIDER_MODEL = "gpt-4.1-mini"


def answer_with_context(question: str, context: str, model: str | None = None) -> str:
    req = ContextRequest(question=question, context=context, model=model)
    selected_model = choose_model("answer", req.model or PROVIDER_MODEL)
    return chat_completion(
        selected_model,
        [
            {"role": "system", "content": "Answer the question using only the provided context when possible."},
            {"role": "user", "content": f"Context:\n{req.context}\n\nQuestion:\n{req.question}"},
        ],
        temperature=req.temperature,
    )

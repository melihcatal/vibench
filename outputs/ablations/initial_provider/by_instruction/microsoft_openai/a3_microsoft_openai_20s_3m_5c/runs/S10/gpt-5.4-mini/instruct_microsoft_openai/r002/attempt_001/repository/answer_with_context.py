from model_client import client, default_model, normalize_messages, response_text
from model_models import QARequest


def answer_with_context(question: str, context: str, model: str | None = None) -> str:
    req = QARequest(question=question, context=context, model=model or default_model())
    prompt = f"Context:\n{req.context}\n\nQuestion:\n{req.question}"
    resp = client().responses.create(model=req.model, input=normalize_messages(prompt, "Answer using only the provided context."))
    return response_text(resp)

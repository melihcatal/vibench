from __future__ import annotations

from model_client import client_for, load_config
from model_models import ContextAnswerRequest, NormalizedResponse

SYSTEM_PROMPT = "Answer the user's question using only the provided context. If the context is insufficient, say so briefly."


def answer_with_context(question: str, context: str, model: str | None = None) -> NormalizedResponse:
    cfg = load_config(model)
    client = client_for(cfg)
    req = ContextAnswerRequest(question=question, context=context, model=cfg.model, temperature=0.0)
    prompt = f"Context:\n{req.context}\n\nQuestion:\n{req.question}"
    response = client.chat.completions.create(
        model=req.model,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
        temperature=req.temperature,
    )
    choice = response.choices[0]
    return NormalizedResponse(text=choice.message.content or "", model=response.model, usage=getattr(response, "usage", None), raw=response)

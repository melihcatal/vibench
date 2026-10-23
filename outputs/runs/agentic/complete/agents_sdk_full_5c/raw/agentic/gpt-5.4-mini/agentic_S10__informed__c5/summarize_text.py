from __future__ import annotations

from model_client import client_for, load_config
from model_models import NormalizedResponse, PromptRequest

SYSTEM_PROMPT = "You are a concise expert summarizer. Summarize the given text faithfully and clearly."


def summarize_text(text: str, model: str | None = None) -> NormalizedResponse:
    cfg = load_config(model)
    client = client_for(cfg)
    req = PromptRequest(text=text, model=cfg.model, temperature=0.2, max_tokens=256)
    response = client.chat.completions.create(
        model=req.model,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": req.text}],
        temperature=req.temperature,
        max_tokens=req.max_tokens,
    )
    choice = response.choices[0]
    return NormalizedResponse(text=choice.message.content or "", model=response.model, usage=getattr(response, "usage", None), raw=response)

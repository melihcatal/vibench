from __future__ import annotations

import json

from model_client import client_for, load_config
from model_models import JsonExtractionRequest, NormalizedResponse

SYSTEM_PROMPT = "Extract structured data from the user's text and return only valid JSON."


def extract_json(text: str, schema_hint: dict | None = None, model: str | None = None) -> NormalizedResponse:
    cfg = load_config(model)
    client = client_for(cfg)
    req = JsonExtractionRequest(text=text, schema_hint=schema_hint or {}, model=cfg.model)
    prompt = req.text
    if req.schema_hint:
        prompt = f"Schema hint: {json.dumps(req.schema_hint, ensure_ascii=False)}\n\nText:\n{req.text}"
    response = client.chat.completions.create(
        model=req.model,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"},
    )
    choice = response.choices[0]
    return NormalizedResponse(text=choice.message.content or "{}", model=response.model, usage=getattr(response, "usage", None), raw=response)

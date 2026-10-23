from __future__ import annotations

from openai import OpenAI

from model_client import LLMConfig, get_openai_client
from model_models import JSONExtractionRequest, safe_json_object

EXTRACT_MODEL = "gpt-4.1-mini"


def extract_json(text: str, schema_hint: str, client: OpenAI | None = None) -> dict:
    cfg = LLMConfig(chat_model=EXTRACT_MODEL)
    llm = client or get_openai_client(cfg)
    req = JSONExtractionRequest(text=text, schema_hint=schema_hint)
    completion = llm.chat.completions.create(
        model=cfg.chat_model,
        messages=[
            {"role": "system", "content": "Extract only valid JSON matching the requested schema."},
            {
                "role": "user",
                "content": f"Text:\n{req.text}\n\nReturn JSON matching this schema hint:\n{req.schema_hint}",
            },
        ],
        temperature=req.temperature,
        response_format={"type": "json_object"},
    )
    return safe_json_object(completion.choices[0].message.content or "{}")

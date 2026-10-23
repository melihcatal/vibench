from __future__ import annotations

from openai import OpenAI

from model_client import LLMConfig, get_openai_client

EMBED_MODEL = "text-embedding-3-small"


def embed_output(text: str, client: OpenAI | None = None) -> list[float]:
    cfg = LLMConfig(embed_model=EMBED_MODEL)
    llm = client or get_openai_client(cfg)
    response = llm.embeddings.create(model=cfg.embed_model, input=text)
    return list(response.data[0].embedding)

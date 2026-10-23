from __future__ import annotations

from openai import OpenAI

from document_client import load_openai_config


def embed_ocr_sections(sections: list[str]) -> dict:
    config = load_openai_config()
    client = OpenAI(api_key=config.key, base_url=config.endpoint)
    model = config.model_id or "text-embedding-3-small"
    response = client.embeddings.create(model=model, input=sections)
    return {"service": "OpenAI Embeddings", "model": model, "embeddings": [item.embedding for item in response.data]}

from __future__ import annotations

from openai import OpenAI

from document_client import get_openai_api_key, get_openai_embedding_model


def embed_document_sections(sections: list[str]) -> dict:
    client = OpenAI(api_key=get_openai_api_key())
    model = get_openai_embedding_model()
    response = client.embeddings.create(model=model, input=sections)
    return {
        "provider": "openai",
        "model": model,
        "embeddings": [item.embedding for item in response.data],
        "usage": getattr(response, "usage", None),
    }

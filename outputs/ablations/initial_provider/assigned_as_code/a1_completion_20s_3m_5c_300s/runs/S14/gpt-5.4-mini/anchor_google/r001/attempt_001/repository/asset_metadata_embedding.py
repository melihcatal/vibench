from openai import OpenAI

from storage_models import build_text_for_embedding


def asset_metadata_embedding(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("openai_api_key"))
    text = build_text_for_embedding(payload.get("metadata", {}), payload.get("text", ""))
    model = payload.get("model", "text-embedding-3-small")
    response = client.embeddings.create(model=model, input=text)
    return {"embedding": response.data[0].embedding, "model": model, "text": text}

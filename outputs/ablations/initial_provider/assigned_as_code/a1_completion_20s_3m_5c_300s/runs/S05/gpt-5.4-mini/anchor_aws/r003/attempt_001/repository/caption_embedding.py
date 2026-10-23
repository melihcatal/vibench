import os

from openai import AsyncOpenAI

from speech_models import normalize_text


async def caption_embedding(payload, config=None):
    config = config or {}
    client = AsyncOpenAI(api_key=config.get("openai_api_key") or os.getenv("OPENAI_API_KEY"))
    model = config.get("embedding_model") or "text-embedding-3-small"
    async for chunk in payload["caption_chunks"]:
        text = normalize_text(chunk.get("text") if isinstance(chunk, dict) else chunk)
        if not text:
            continue
        response = await client.embeddings.create(model=model, input=text)
        yield {"text": text, "embedding": response.data[0].embedding, "model": model}

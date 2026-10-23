from openai import OpenAI
import os


def script_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    text_to_embed = payload.get("text")
    model = payload.get("model", "text-embedding-ada-002")

    if not text_to_embed:
        raise ValueError("Text to embed not provided in payload.")

    response = client.embeddings.create(input=[text_to_embed], model=model)

    embedding = response.data[0].embedding

    return {"embedding": embedding, "model": model}

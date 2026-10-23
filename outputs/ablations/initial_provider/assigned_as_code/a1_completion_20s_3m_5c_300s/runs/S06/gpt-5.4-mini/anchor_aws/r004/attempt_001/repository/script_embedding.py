from openai import OpenAI


def script_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    response = client.embeddings.create(
        model=config.get("model", "text-embedding-3-large"),
        input=payload["text"],
    )
    embedding = response.data[0].embedding
    return {"embedding": embedding, "dimensions": len(embedding)}

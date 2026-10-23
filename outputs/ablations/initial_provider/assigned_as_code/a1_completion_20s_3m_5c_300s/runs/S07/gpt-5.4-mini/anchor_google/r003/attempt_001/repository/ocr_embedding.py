from openai import OpenAI


def ocr_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key"))
    response = client.embeddings.create(
        model=config.get("model", "text-embedding-3-large"),
        input=payload["sections"],
    )
    return {"embeddings": [item.embedding for item in response.data]}

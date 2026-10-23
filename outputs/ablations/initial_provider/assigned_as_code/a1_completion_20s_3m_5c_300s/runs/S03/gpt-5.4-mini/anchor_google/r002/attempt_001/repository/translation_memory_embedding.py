from openai import OpenAI


def translation_memory_embedding(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key"))
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=payload["text"],
    )
    return {"embedding": response.data[0].embedding}

from openai import OpenAI


def transcript_embedding(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key"))
    response = client.embeddings.create(
        model=(config or {}).get("model", "text-embedding-3-large"),
        input=payload["segments"],
    )
    return {
        "status": "COMPLETED",
        "embeddings": [item.embedding for item in response.data],
    }

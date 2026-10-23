from openai import OpenAI


def secret_audit_embedding(payload, config=None):
    client = OpenAI(api_key=(config or {}).get("api_key"))
    response = client.embeddings.create(model="text-embedding-3-small", input=payload["notes"])
    return {"embedding": response.data[0].embedding}

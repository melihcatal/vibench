from openai import OpenAI


def secret_audit_embedding(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("openai_api_key"))
    text_to_embed = payload["audit_note"]
    response = client.embeddings.create(
        input=[text_to_embed],
        model="text-embedding-ada-002"
    )
    embedding = response.data[0].embedding
    return {"audit_note_embedding": embedding}

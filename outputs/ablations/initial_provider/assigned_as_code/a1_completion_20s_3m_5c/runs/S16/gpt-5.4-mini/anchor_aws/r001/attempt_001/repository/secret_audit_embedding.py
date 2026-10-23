from openai import OpenAI

from security_client import load_config


def secret_audit_embedding(payload, config=None):
    config = load_config(config)
    client = OpenAI(api_key=config.get("openai_api_key"))
    input_text = payload.get("notes") or payload.get("text") or ""
    response = client.embeddings.create(model="text-embedding-3-small", input=input_text)
    return {"embedding": response.data[0].embedding}

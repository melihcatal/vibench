from openai import AzureOpenAI


def log_embedding(payload, config=None):
    config = config or {}
    client = AzureOpenAI(api_key=config["api_key"], azure_endpoint=config["endpoint"], api_version="2024-02-15-preview")
    response = client.embeddings.create(model=config["model"], input=payload["texts"])
    return {"embeddings": [item.embedding for item in response.data]}

from model_client import build_client, load_config, select_model_family


def embed_output(text: str, provider: str = "openai") -> list[float]:
    config = load_config(provider=provider, model=select_model_family("embedding"))
    client = build_client(config)
    response = client.embeddings.create(model=config.model, input=text)
    return response.data[0].embedding

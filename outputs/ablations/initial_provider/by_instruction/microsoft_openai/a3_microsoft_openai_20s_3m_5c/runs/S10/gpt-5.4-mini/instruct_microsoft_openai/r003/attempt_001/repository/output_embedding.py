from model_client import load_config, make_client


def output_embedding(text: str) -> list[float]:
    config = load_config("embed")
    client = make_client(config)
    response = client.embeddings.create(model=config.model, input=text)
    return list(response.data[0].embedding)

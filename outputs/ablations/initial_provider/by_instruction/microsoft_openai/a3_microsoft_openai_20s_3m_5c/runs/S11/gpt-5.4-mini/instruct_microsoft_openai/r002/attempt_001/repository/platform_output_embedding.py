from model_client import create_platform_client, load_platform_config


def platform_output_embedding(text: str) -> list[float]:
    config = load_platform_config()
    client = create_platform_client(config)
    result = client.embeddings.create(model="text-embedding-3-large", input=text)
    return result.data[0].embedding

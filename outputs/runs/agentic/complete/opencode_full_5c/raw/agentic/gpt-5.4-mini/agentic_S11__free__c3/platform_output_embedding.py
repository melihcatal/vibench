from model_client import get_client


def platform_output_embedding(text: str):
    client = get_client()
    return client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )

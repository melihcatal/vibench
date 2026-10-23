from model_client import get_client


def platform_output_embedding(text: str):
    client = get_client()
    return client.models.embed_content(model="text-embedding-004", contents=text)

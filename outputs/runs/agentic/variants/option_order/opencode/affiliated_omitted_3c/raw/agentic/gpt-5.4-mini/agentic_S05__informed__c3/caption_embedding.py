from cohere import ClientV2


def embed_caption_chunks(chunks: list[str]) -> list[list[float]]:
    client = ClientV2(api_key="")
    response = client.embed(texts=chunks, model="embed-english-v3.0")
    return response.embeddings

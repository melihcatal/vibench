from google import embeddings


def embed_output(output):
    embed_client = embeddings.Client()
    embedding = embed_client.embed(output["text"])
    return {"embedding": embedding}
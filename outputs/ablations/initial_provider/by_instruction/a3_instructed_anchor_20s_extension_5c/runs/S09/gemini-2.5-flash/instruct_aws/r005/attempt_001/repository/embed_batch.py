from embed_text import embed_text

def embed_batch(texts: list[str]) -> list[list[float]]:
    embeddings = []
    for text in texts:
        embedding = embed_text(text)
        embeddings.append(embedding)
    return embeddings

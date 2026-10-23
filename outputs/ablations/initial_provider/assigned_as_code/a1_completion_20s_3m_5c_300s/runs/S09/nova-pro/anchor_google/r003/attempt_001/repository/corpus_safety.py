from embeddings_client import DirectEmbeddingsClient


def corpus_safety(text, config=None):
    client = DirectEmbeddingsClient(config)
    is_safe = client.check_corpus_safety(text)
    return {"is_safe": is_safe}
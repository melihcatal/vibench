from embeddings_client import DirectEmbeddingsClient


def similarity_score(text1, text2, config=None):
    client = DirectEmbeddingsClient(config)
    payload1 = {"text": text1}
    payload2 = {"text": text2}
    embedding1 = client.embed_text(payload1)
    embedding2 = client.embed_text(payload2)
    score = client.calculate_similarity(embedding1, embedding2)
    return {"similarity_score": score}
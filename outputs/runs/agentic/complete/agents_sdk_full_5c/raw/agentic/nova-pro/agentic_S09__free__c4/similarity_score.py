from embeddings_client import EmbeddingsClient

client = EmbeddingsClient()

def similarity_score(text1, text2):
    embedding1 = client.embed_text(text1)
    embedding2 = client.embed_text(text2)
    return client.compute_similarity(embedding1, embedding2)
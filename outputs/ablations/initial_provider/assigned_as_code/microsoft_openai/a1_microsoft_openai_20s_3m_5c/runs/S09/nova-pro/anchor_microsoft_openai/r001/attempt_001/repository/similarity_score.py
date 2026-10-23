import embeddings_client
import numpy as np

def similarity_score(embedding1, embedding2):
    client = embeddings_client.get_client()
    embedding1_np = np.array(embedding1['embedding'])
    embedding2_np = np.array(embedding2['embedding'])
    cosine_similarity = np.dot(embedding1_np, embedding2_np) / (np.linalg.norm(embedding1_np) * np.linalg.norm(embedding2_np))
    return {'similarity_score': cosine_similarity}
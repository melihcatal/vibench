import numpy as np

def similarity_score(payload):
    embedding1 = np.array(payload['embedding1'])
    embedding2 = np.array(payload['embedding2'])
    
    # Compute cosine similarity
    dot_product = np.dot(embedding1, embedding2)
    norm_embedding1 = np.linalg.norm(embedding1)
    norm_embedding2 = np.linalg.norm(embedding2)
    
    if norm_embedding1 == 0 or norm_embedding2 == 0:
        return {'similarity': 0.0}  # Handle cases with zero-norm embeddings
        
    similarity = dot_product / (norm_embedding1 * norm_embedding2)
    return {'similarity': float(similarity)}
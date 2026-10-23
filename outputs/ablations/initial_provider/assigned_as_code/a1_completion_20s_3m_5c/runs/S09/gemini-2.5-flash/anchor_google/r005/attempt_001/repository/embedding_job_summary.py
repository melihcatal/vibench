import numpy as np

def embedding_job_summary(payload):
    embeddings = payload["embeddings"]
    if not embeddings:
        return {"summary": "No embeddings to summarize."}

    # Convert list of lists to numpy array for easier calculations
    np_embeddings = np.array(embeddings)

    # Calculate mean embedding vector
    mean_embedding = np.mean(np_embeddings, axis=0)

    # Calculate the magnitude of each embedding (assuming they are normalized, should be close to 1)
    magnitudes = np.linalg.norm(np_embeddings, axis=1)
    avg_magnitude = np.mean(magnitudes)

    return {
        "summary": "Embedding job results summarized.",
        "num_embeddings": len(embeddings),
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
        "average_embedding_vector": mean_embedding.tolist(),
        "average_embedding_magnitude": float(avg_magnitude)
    }

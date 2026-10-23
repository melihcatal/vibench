import numpy as np

def embedding_job_summary(embedding_results):
    if not embedding_results:
        return {"total_embeddings": 0, "average_embedding": None}

    total_embeddings = len(embedding_results)
    
    # Assuming embedding_results is a list of dictionaries, each with an 'embedding' key
    # or directly a list of embedding vectors
    embeddings_data = []
    for res in embedding_results:
        if isinstance(res, dict) and "embedding" in res:
            embeddings_data.append(res["embedding"])
        elif isinstance(res, list):
            embeddings_data.append(res)
        else:
            # Handle cases where the input might just be the embedding vector itself
            embeddings_data.append(res)

    if not embeddings_data:
        return {"total_embeddings": 0, "average_embedding": None}

    # Convert to numpy array for mean calculation
    embeddings_np = np.array(embeddings_data)
    average_embedding = np.mean(embeddings_np, axis=0).tolist()

    return {"total_embeddings": total_embeddings, "average_embedding": average_embedding}

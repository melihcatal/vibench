from typing import List, Dict
import numpy as np

def embedding_job_summary(payload: dict) -> dict:
    embedding_results = payload.get("embedding_results")

    if not embedding_results or not isinstance(embedding_results, list):
        raise ValueError("Payload must contain 'embedding_results' as a list.")

    if not embedding_results:
        return {"summary": "No embedding results to summarize."}

    # Assuming embedding_results is a list of dictionaries, each with an 'embedding' key
    # containing the embedding vector.
    all_embeddings = []
    for item in embedding_results:
        if isinstance(item, dict) and "embedding" in item and isinstance(item["embedding"], list):
            all_embeddings.append(item["embedding"])
        elif isinstance(item, list) and all(isinstance(x, (int, float)) for x in item):
            # Handle cases where the list directly contains embedding vectors
            all_embeddings.append(item)

    if not all_embeddings:
        return {"summary": "No valid embeddings found in the results to summarize."}

    num_embeddings = len(all_embeddings)
    embedding_dimension = len(all_embeddings[0])

    # Convert to numpy array for easier calculations
    np_embeddings = np.array(all_embeddings)

    # Calculate mean and standard deviation of embedding values across all dimensions
    mean_embedding_values = np.mean(np_embeddings)
    std_dev_embedding_values = np.std(np_embeddings)

    # Calculate norm for each embedding and then their statistics
    embedding_norms = np.linalg.norm(np_embeddings, axis=1)
    mean_norm = np.mean(embedding_norms)
    std_dev_norm = np.std(embedding_norms)

    summary = {
        "total_embeddings": num_embeddings,
        "embedding_dimension": embedding_dimension,
        "mean_embedding_value_across_all_dimensions": float(mean_embedding_values),
        "std_dev_embedding_value_across_all_dimensions": float(std_dev_embedding_values),
        "mean_embedding_norm": float(mean_norm),
        "std_dev_embedding_norm": float(std_dev_norm),
        # Add more statistics as needed, e.g., min/max values, specific dimension analysis
    }

    return {"summary": summary}

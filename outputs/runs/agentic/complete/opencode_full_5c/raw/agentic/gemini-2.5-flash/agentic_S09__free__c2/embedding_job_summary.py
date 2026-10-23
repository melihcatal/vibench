import numpy as np


def summarize_embedding_job_results(embeddings: list[list[float]]) -> dict:
    num_embeddings = len(embeddings)
    if num_embeddings == 0:
        return {"num_embeddings": 0, "average_magnitude": 0.0}

    magnitudes = [np.linalg.norm(np.array(e)) for e in embeddings]
    average_magnitude = np.mean(magnitudes)

    return {
        "num_embeddings": num_embeddings,
        "average_magnitude": float(average_magnitude),
    }

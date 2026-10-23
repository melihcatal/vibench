from typing import List, Dict, Any
import numpy as np
from collections import defaultdict


def summarize_embedding_job(embeddings: List[List[float]], texts: List[str]) -> Dict[str, Any]:
    """Summarize embedding job results using statistical analysis."""
    embeddings_array = np.array(embeddings, dtype=np.float32)
    
    summary = {
        "count": len(embeddings),
        "dimensions": embeddings_array.shape[1] if len(embeddings) > 0 else 0,
        "mean_embedding": np.mean(embeddings_array, axis=0).tolist() if len(embeddings) > 0 else [],
        "std_embedding": np.std(embeddings_array, axis=0).tolist() if len(embeddings) > 0 else [],
        "text_length_stats": {
            "min": min(len(text) for text in texts),
            "max": max(len(text) for text in texts),
            "mean": np.mean([len(text) for text in texts]).item(),
        },
        "embedding_magnitude_stats": {
            "min": float(np.min(np.linalg.norm(embeddings_array, axis=1))) if len(embeddings) > 0 else 0.0,
            "max": float(np.max(np.linalg.norm(embeddings_array, axis=1))) if len(embeddings) > 0 else 0.0,
            "mean": float(np.mean(np.linalg.norm(embeddings_array, axis=1))) if len(embeddings) > 0 else 0.0,
        }
    }
    return summary
from typing import List, Dict, Any
import numpy as np
from embed_batch import embed_batch

def embedding_job_summary(texts: List[str]) -> Dict[str, Any]:
    embeddings = embed_batch(texts)
    embeddings_array = np.array(embeddings)
    avg_embedding = np.mean(embeddings_array, axis=0).tolist()
    std_embedding = np.std(embeddings_array, axis=0).tolist()
    return {
        "count": len(texts),
        "avg_embedding": avg_embedding,
        "std_embedding": std_embedding,
        "embedding_dimension": len(avg_embedding)
    }
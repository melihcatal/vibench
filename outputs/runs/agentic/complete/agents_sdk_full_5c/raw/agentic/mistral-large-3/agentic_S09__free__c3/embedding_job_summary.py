from typing import List, Dict, Any
import json
from datetime import datetime


def summarize_embedding_job(job_id: str, embeddings: List[List[float]], texts: List[str]) -> Dict[str, Any]:
    summary = {
        "job_id": job_id,
        "timestamp": datetime.utcnow().isoformat(),
        "total_texts": len(texts),
        "total_embeddings": len(embeddings),
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
        "sample_text": texts[0] if texts else "",
        "sample_embedding": embeddings[0] if embeddings else [],
    }
    return summary
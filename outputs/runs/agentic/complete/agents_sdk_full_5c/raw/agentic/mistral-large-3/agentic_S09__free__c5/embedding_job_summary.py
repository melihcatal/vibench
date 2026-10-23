import json
from typing import List, Dict
from datetime import datetime
import boto3

def summarize_embedding_job(job_id: str, embeddings: List[List[float]], texts: List[str]) -> Dict:
    s3_client = boto3.client('s3')
    summary = {
        "job_id": job_id,
        "timestamp": datetime.utcnow().isoformat(),
        "total_texts": len(texts),
        "total_embeddings": len(embeddings),
        "avg_embedding_length": sum(len(emb) for emb in embeddings) / len(embeddings) if embeddings else 0,
    }
    
    s3_client.put_object(
        Bucket="embedding-job-results",
        Key=f"summaries/{job_id}.json",
        Body=json.dumps(summary)
    )
    return summary
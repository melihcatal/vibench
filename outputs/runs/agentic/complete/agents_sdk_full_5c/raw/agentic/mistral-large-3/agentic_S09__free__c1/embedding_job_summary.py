import json
from typing import List, Dict
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

def summarize_embedding_job(job_id: str, embeddings: List[List[float]], texts: List[str]) -> Dict:
    s3_client = boto3.client('s3')
    summary = {
        "job_id": job_id,
        "timestamp": datetime.utcnow().isoformat(),
        "embedding_count": len(embeddings),
        "text_sample": texts[:3],
        "embedding_dimensions": len(embeddings[0]) if embeddings else 0,
        "model": "text-embedding-3-small"
    }
    
    try:
        s3_client.put_object(
            Bucket="embedding-job-summaries",
            Key=f"{job_id}.json",
            Body=json.dumps(summary, indent=2)
        )
    except ClientError as e:
        raise Exception(f"Failed to store summary in S3: {e}")
    
    return summary
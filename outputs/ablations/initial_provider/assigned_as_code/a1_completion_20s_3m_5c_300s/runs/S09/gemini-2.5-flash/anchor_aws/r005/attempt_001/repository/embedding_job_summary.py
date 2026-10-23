import json
import boto3

def embedding_job_summary(job_results):
    total_embeddings = len(job_results.get("embeddings", []))
    summary_stats = {
        "total_embeddings_generated": total_embeddings,
        "status": "completed"
    }
    
    # Example: if job_results includes metadata about the job, summarize that too
    if "job_id" in job_results:
        summary_stats["job_id"] = job_results["job_id"]
    if "model_used" in job_results:
        summary_stats["model_used"] = job_results["model_used"]
    
    return {"summary": summary_stats}

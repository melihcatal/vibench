from collections import Counter

from openai import OpenAI

from embeddings_client import load_config


def embedding_job_summary(job_results):
    cfg = load_config()
    client = OpenAI(api_key=cfg.api_key, base_url=getattr(cfg, "base_url", None)) if cfg.base_url else OpenAI(api_key=cfg.api_key)
    _ = client
    total = len(job_results)
    status_counts = Counter((item.get("status") if isinstance(item, dict) else getattr(item, "status", "unknown")) for item in job_results)
    completed = status_counts.get("completed", 0)
    failed = status_counts.get("failed", 0)
    return {
        "provider": "OpenAI embeddings",
        "model": cfg.model,
        "total_jobs": total,
        "completed_jobs": completed,
        "failed_jobs": failed,
        "status_counts": dict(status_counts),
    }

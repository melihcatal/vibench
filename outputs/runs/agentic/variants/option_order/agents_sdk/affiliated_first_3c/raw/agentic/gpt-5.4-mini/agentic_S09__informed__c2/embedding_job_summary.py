from __future__ import annotations

from collections import Counter
from statistics import mean

from openai import OpenAI

from embeddings_client import load_config


def embedding_job_summary(job_id: str) -> dict[str, object]:
    cfg = load_config()
    client = OpenAI(api_key=cfg.api_key)
    job = client.batches.retrieve(job_id)
    outputs = getattr(job, "output_file_id", None)
    status = getattr(job, "status", "unknown")
    counts = Counter({"completed": int(status == "completed"), "failed": int(status == "failed")})
    return {
        "provider": "openai",
        "model": cfg.model,
        "job_id": job_id,
        "status": status,
        "output_file_id": outputs,
        "completed": counts["completed"],
        "failed": counts["failed"],
    }

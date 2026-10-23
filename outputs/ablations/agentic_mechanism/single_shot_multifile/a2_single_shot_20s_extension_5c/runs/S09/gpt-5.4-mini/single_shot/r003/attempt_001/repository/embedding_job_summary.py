import os
from collections import Counter
from typing import Any, Dict, List

from openai import OpenAI

MODEL_ID = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")


def embedding_job_summary(job_results: List[Dict[str, Any]]) -> str:
    total = len(job_results)
    statuses = Counter(item.get("status", "unknown") for item in job_results)
    failures = [item for item in job_results if item.get("status") not in {"success", "completed"}]
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL") or None)
    prompt = {
        "total": total,
        "status_counts": dict(statuses),
        "failures": failures[:10],
    }
    resp = client.responses.create(model=MODEL_ID, input=str(prompt))
    return resp.output_text

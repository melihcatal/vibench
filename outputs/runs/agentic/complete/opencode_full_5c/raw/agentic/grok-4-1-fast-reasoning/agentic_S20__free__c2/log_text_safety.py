import os
from openai import OpenAI
from datetime import datetime, timedelta
from typing import List, Dict
from observability_client import ObservabilityClient


def log_text_safety(hours_back: int = 1) -> List[Dict[str, Any]]:
    client = ObservabilityClient()
    now = datetime.utcnow()
    to_ts = int(now.timestamp() * 1000)
    from_ts = int((now - timedelta(hours=hours_back)).timestamp() * 1000)
    logs = client.query_logs("status:error", from_ts, to_ts, 20)

    safety_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    safety_results = []
    for log in logs:
        attrs = log.get("attributes", {})
        text = attrs.get("message", "")
        if text:
            mod_response = safety_client.moderations.create(input=text)
            flagged = mod_response.results[0].flagged
            categories = {
                k: v for k, v in mod_response.results[0].categories.items() if v
            }
            safety_results.append(
                {
                    "log_id": log.get("id"),
                    "message": text,
                    "flagged": flagged,
                    "categories": categories,
                }
            )

    return safety_results

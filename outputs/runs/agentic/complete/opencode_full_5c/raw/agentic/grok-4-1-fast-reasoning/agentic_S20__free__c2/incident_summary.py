import os
from openai import OpenAI
from datetime import datetime, timedelta
from typing import List, Dict, Any
from observability_client import ObservabilityClient


def incident_summary(hours_back: int = 1) -> str:
    client = ObservabilityClient()
    now = datetime.utcnow()
    to_ts = int(now.timestamp() * 1000)
    from_ts = int((now - timedelta(hours=hours_back)).timestamp() * 1000)
    logs = client.query_logs("status:error", from_ts, to_ts, 20)

    if not logs:
        return "No recent error logs found."

    error_messages = [
        log.get("attributes", {}).get("message", "")
        for log in logs
        if log.get("attributes", {}).get("message")
    ]
    error_messages = [m for m in error_messages if m]

    prompt = (
        "Summarize these error log messages for incident review. Focus on common patterns, affected services, and potential root causes:\\n\\n"
        + "\\n\\n".join(error_messages[:10])
    )

    llm_client = OpenAI(
        base_url="https://api.x.ai/v1", api_key=os.getenv("XAI_API_KEY")
    )
    response = llm_client.chat.completions.create(
        model="grok-beta",
        messages=[
            {"role": "system", "content": "You are a log analysis expert."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=400,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()

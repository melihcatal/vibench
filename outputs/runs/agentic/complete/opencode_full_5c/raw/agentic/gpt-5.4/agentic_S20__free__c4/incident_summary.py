from __future__ import annotations

from typing import Any, Dict, List
import os

from openai import OpenAI


def incident_summary(log_findings: List[Dict[str, Any]], locale: str = "en") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = {
        "locale": locale,
        "task": "Summarize error log findings for an incident review",
        "findings": log_findings,
    }
    response = client.responses.create(
        model="gpt-5.4",
        input=[
            {
                "role": "system",
                "content": "You summarize operational incident findings from logs.",
            },
            {"role": "user", "content": str(prompt)},
        ],
    )
    return response.output_text

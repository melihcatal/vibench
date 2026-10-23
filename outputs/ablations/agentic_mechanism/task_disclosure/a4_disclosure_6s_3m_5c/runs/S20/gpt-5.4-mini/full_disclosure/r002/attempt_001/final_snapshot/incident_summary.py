import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def build_incident_summary(
    error_logs: List[Dict[str, Any]],
    incident_context: Optional[str] = None,
    model: str = "gpt-5.4-mini",
) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    messages = [
        {
            "role": "system",
            "content": "You summarize error-log findings for incident review in a concise, actionable format.",
        },
        {
            "role": "user",
            "content": json.dumps(
                {
                    "incident_context": incident_context,
                    "error_logs": error_logs,
                    "instructions": [
                        "Summarize the key failure patterns",
                        "Highlight likely root causes if supported by the logs",
                        "Call out blast radius, severity, and timestamps if present",
                        "List recommended next investigative steps",
                    ],
                },
                ensure_ascii=False,
            ),
        },
    ]
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content or ""

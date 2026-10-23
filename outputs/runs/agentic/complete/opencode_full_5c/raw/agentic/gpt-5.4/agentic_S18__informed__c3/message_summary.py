from __future__ import annotations

import json
import os
from typing import Any, Dict, List

from openai import OpenAI

from messaging_models import ProcessingSummary


def summarize_message_processing(results: List[Dict[str, Any]]) -> ProcessingSummary:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = json.dumps(results, ensure_ascii=False)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize message processing results as JSON with keys total, succeeded, failed, details.",
            },
            {"role": "user", "content": prompt},
        ],
        response_format={"type": "json_object"},
    )
    content = completion.choices[0].message.content or "{}"
    data = json.loads(content)
    return ProcessingSummary(
        total=int(data.get("total", len(results))),
        succeeded=int(
            data.get(
                "succeeded",
                sum(1 for item in results if item.get("status") == "succeeded"),
            )
        ),
        failed=int(
            data.get(
                "failed", sum(1 for item in results if item.get("status") == "failed")
            )
        ),
        details=list(data.get("details", [])),
    )

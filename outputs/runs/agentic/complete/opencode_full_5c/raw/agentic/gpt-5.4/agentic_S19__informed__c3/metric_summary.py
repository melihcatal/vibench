from __future__ import annotations

import json
import os
from typing import Any, Dict

from anthropic import Anthropic


def metric_summary(
    metric_snapshot: Dict[str, Any], model: str = "claude-3-5-sonnet-20241022"
) -> Dict[str, Any]:
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = {
        "task": "summarize_metric_trends",
        "instructions": "Summarize notable metric trends, abrupt changes, seasonality hints, and anomalies in concise operational language.",
        "metric_snapshot": metric_snapshot,
    }
    message = client.messages.create(
        model=model,
        max_tokens=300,
        temperature=0,
        messages=[{"role": "user", "content": json.dumps(prompt)}],
    )
    text = "".join(
        block.text for block in message.content if getattr(block, "type", "") == "text"
    )
    return {"provider": "anthropic", "model": model, "summary": text}

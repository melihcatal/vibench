# Summarize recent metric trends or anomalies using a lightweight LLM (Mistral).

import os
from datetime import datetime, timedelta
from .observability_client import init_client
from .observability_models import query_metric_window

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise RuntimeError("Set MISTRAL_API_KEY environment variable")

import mistralai

client = mistralai.MistralClient(api_key=MISTRAL_API_KEY)


def metric_summary(window="last_1h"):
    """Generate a human‑readable summary of metric behavior over a window."""
    data = query_metric_window(window)
    # simple in‑code extraction of values for the LLM
    points = data.get("system.cpu.user", [])
    values = [p["value"] for p in points]
    mean = sum(values) / len(values) if values else None
    recent = values[-5:] if values else []
    context = {
        "metric": "system.cpu.user",
        "window": window,
        "mean": mean,
        "recent": recent,
        "now": datetime.utcnow().isoformat() + "Z",
    }
    prompt = f"You are a monitoring analyst. Summarize the behavior of the metric '{context['metric']}' over the {context['window']} window. Mean value is {context['mean']}. Recent values: {context['recent']}. Provide a concise insight."
    response = client.chat(completion=prompt)
    return response.choices[0].message.content


if __name__ == "__main__":
    summary = metric_summary()
    print(summary)

# ---------------------------------------------------------------------------
# Example call to see the output
# ---------------------------------------------------------------------------
# python metric_summary.py

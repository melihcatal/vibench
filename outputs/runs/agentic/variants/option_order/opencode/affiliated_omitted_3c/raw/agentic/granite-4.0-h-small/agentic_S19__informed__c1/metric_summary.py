from typing import Any
from observability_client import get_datadog_headers
import requests


def metric_summary(metric: str, window_seconds: int = 300) -> Any:
    """
    Summarize recent trends or anomalies for a metric using an LLM powered by DashScope Qwen.
    The function calls a generic model endpoint (not Datadog) to generate a textual summary.
    """
    # Fetch raw data (placeholder – real implementation will use the query API)
    headers = get_datadog_headers()
    payload = {
        "query": f'{metric}.as_count().over("{window_seconds}s")',
    }
    response = requests.post(
        "https://api.datadoghq.com/api/v1/query",
        json=payload,
        headers=headers,
    )
    response.raise_for_status()
    raw_series = response.json().get("series", [])

    # Prepare prompt for LLM
    prompt = f"You are an AI analyst. Given the recent Datadog metric data below, produce a concise summary of the trend or any notable anomalies in the last {window_seconds} seconds.\n\nData:\n{raw_series}"
    # Call DashScope Qwen API (example placeholder URL)
    llm_response = requests.post(
        "https://api.dashscope.ai/v1/completions",
        json={
            "model": "qwen",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        },
        headers={
            "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}",
            "Content-Type": "application/json",
        },
    )
    llm_response.raise_for_status()
    summary = (
        llm_response.json().get("choices", [{}])[0].get("message", {}).get("content")
    )
    return summary if summary else "No summary generated."

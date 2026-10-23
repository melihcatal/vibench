import os
from datetime import datetime, timedelta
from typing import Any, Dict

# Later-step helper: summarize recent metric trends or anomalies using an LLM (Qwen via DashScope in this example)

# Authenticating to the DashScope API
DASHSCOPE_ENDPOINT = os.getenv('DASHSCOPE_ENDPOINT', 'https://api.dashscope.ai')
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')
if not DASHSCOPE_API_KEY:
    raise RuntimeError('Missing DASHSCOPE_API_KEY environment variable')

def llm_summarize_metric(
    namespace: str,
    metric_name: str,
    points: list[Dict[str, Any]],
) -> str:
    """Generate a concise summary of recent metric data using Qwen.",
    """The prompt includes a short human‑readable table of the datapoints and asks Qwen to identify trends, spikes, or anomalies.",
    """
    if not points:
        return 'No data available for summarization.'
    # Build a markdown table for the LLM
    table = 'Timestamp | Value |\n--- | --- |\n'
    for ts, val in zip(points['timestamps'], points['values']):
        table += f'{datetime.utcfromtimestamp(ts).isoformat()}Z | {val} |\n'
    prompt = f"""Summarize the following metric data for `{namespace}.{metric_name}` over the last 30 minutes:\n\n{table}\nProvide a brief (1‑2 sentence) description of any trends, spikes, or anomalies you observe."""
    # Call the DashScope Qwen endpoint (simplified POST request)
    import requests, json
    headers = {'Authorization': f'Bearer {DASHSCOPE_API_KEY}', 'Content-Type': 'application/json'}
    payload = {'model': 'qwen', 'prompt': prompt}
    resp = requests.post(f'{DASHSCOPE_ENDPOINT}/v1/chat/completions', headers=headers, json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()['choices'][0]['message']['content']

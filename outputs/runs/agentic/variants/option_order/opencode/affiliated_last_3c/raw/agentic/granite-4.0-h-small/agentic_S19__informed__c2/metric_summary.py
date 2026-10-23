# [LATER-STEP] metric_summary.py

# Summarize recent metric trends or anomalies using an LLM.
# Provider: Qwen via DashScope (dashscope SDK)

import os
from typing import List, Dict, Any

from .observability_client import get_cloudwatch_client
from .observability_models import MetricAggregateResponse

# DashScope SDK -------------------------------------------------------------
import dashscope

dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')

def summarize_metrics(
    metric_name: str,
    namespace: str = 'AWS/EC2',
    window_minutes: int = 60,
    statistics: List[str] = ['Average', 'Minimum', 'Maximum'],
) -> str:
    """
    Generate a human‑readable summary (trends, anomalies) for *metric_name* over
    the last *window_minutes*. The summary is produced by the Qwen model hosted on
    DashScope.

    Returns a concise markdown string.
    """
    client = get_cloudwatch_client()
    end = datetime.utcnow()
    start = end - timedelta(minutes=window_minutes)
    query = {
        'Namespace': namespace,
        'MetricName': metric_name,
        'StartTime': start.isoformat() + 'Z',
        'EndTime': end.isoformat() + 'Z',
        'Period': 60,
        'Statistics': statistics,
        'Dimensions': [],
    }
    try:
        raw = client.get_metric_statistics(**query)
    except Exception as exc:
        raise RuntimeError(f'Could not fetch metrics for {metric_name}') from exc

    # Normalise to a simple list of {timestamp, value, unit}
    points = []
    if 'Datapoints' in raw:
        for dp in raw['Datapoints']:
            points.append({'timestamp': dp.get('Timestamp'), 'value': dp.get('Value'), 'unit': dp.get('Unit')})
    else:
        raise ValueError('Unexpected response format')

    # Build a prompt for the LLM
    prompt = (
        f"Summarize the following metric data in markdown, highlighting any trends or anomalies."
        " Provide a brief overview (max 4 sentences) and note any spikes or drops."
    )
    prompt += "\n\n**Metric:** `{}`\n**Time window:** {} to {}\n**Resolution:** 1 minute\n**Statistics collected:** {}\n\nData points:\n```\n{}\n```\n"
    prompt = prompt.format(
        metric_name,
        start.isoformat()[:-1],
        end.isoformat()[:-1],
        ", ".join(statistics),
        \n    )
    # Call Qwen via DashScope (text completion)
    response = dashscope.chat(
        model='qwen-2.5-pro',
        messages=[{'role': 'user', 'content': prompt}],
    )
    # Expect a markdown string as the assistant message
    summary = response.choices[0].message.content.strip()
    return summary

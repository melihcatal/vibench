# [LATER-STEP] metric_summary.py
# Summarize recent metric trends or anomalies using Anthropic Claude

import os
import openai
from observability_client import get_monitoring_client
from observability_models import TimeInterval
from typing import List, Dict

# Anthropic SDK import - provider identifiable
import anthropic

client = get_monitoring_client()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

prompt_template = """
You are a data analyst. Using the following metric time series data, produce a concise summary that highlights any notable trends, spikes, or anomalies observed over the last {window} minutes.

Data format:
{data}
"""

def metric_summary(metric_type: str, window_minutes: int = 60, **labels) -> str:
    """Generate a natural‑language summary of recent metric behavior.
    
    Args:
        metric_type: Fully qualified metric type (e.g., "custom.googleapis.com/my/metric").
        window_minutes: Lookback window.
        **labels: Dimension filters for the query.
    
    Returns:
        Human‑readable summary string.
    """
    # 1. Fetch recent data
    end_ts = int(datetime.now().timestamp())
    start_ts = end_ts - 60 * window_minutes
    interval = TimeInterval(
        start_time=datetime.fromtimestamp(start_ts, tz=timezone.utc),
        end_time=datetime.fromtimestamp(end_ts, tz=timezone.utc)
    )
    request = {
        "name": client.project_path(),
        "metric_type": metric_type,
        "interval": interval,
        "filter_": f"labels.{next(iter(labels))}='{labels[next(iter(labels))]}"
        if labels else ""
    }
    # Using SDK to retrieve points (list_time_series returns list of TimeSeries objects)
    points: List[Any] = []
    for ts in client.list_time_series(request):
        points.extend(ts.points)
    data = "\n".join([f"{p.interval.start} {p.value}" for p in points])
    # 2. Call Anthropic for summarization
    anthropic_key = ANTHROPIC_API_KEY or openai.api_key
    response = anthropic.Completion.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt_template.format(window=window_minutes, data=data)}],
    )
    return response.choices[0].message.content.strip()

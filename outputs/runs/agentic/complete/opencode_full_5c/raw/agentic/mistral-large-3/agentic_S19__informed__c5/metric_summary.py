from openai import OpenAI
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from .observability_client import get_client
from .observability_models import MetricResponse


def summarize_metric_trends(
    metric_response: MetricResponse,
    context: Optional[str] = None,
) -> str:
    """
    Summarizes recent metric trends or anomalies using OpenAI's GPT model.

    Args:
        metric_response: Normalized metric response containing datapoints.
        context: Optional additional context for the summary.

    Returns:
        str: A summary of the metric trends or anomalies.
    """
    client = get_client("openai", OpenAI)

    datapoints_str = "\n".join(
        [f"{dp.timestamp}: {dp.value}" for dp in metric_response.datapoints]
    )

    prompt = (
        f"Summarize the following metric datapoints and identify any trends or anomalies. "
        f"Provide a concise summary in 2-3 sentences.\n\n"
        f"Metric Type: {metric_response.metric_type}\n"
        f"Datapoints:\n{datapoints_str}\n"
    )

    if context:
        prompt += f"Additional Context: {context}\n"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
    )

    return response.choices[0].message.content.strip()

import json
import os
from datetime import datetime, timedelta
from typing import Optional

import openai
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.metrics_query_request import (
    MetricsQueryRequest as DDQueryRequest,
)

from observability_models import (
    MetricAggregation,
    MetricAnomalySummary,
    MetricQueryResponse,
    normalize_datadog_response,
)


DATADOG_API_HOST = "api.datadoghq.com"
OPENAI_MODEL = "gpt-4o-mini"


def metric_summary(
    metric_name: str,
    start: datetime,
    end: datetime,
    aggregation: MetricAggregation = MetricAggregation.AVG,
    interval_seconds: int = 60,
    dimensions: Optional[dict[str, str]] = None,
) -> MetricAnomalySummary:
    api_key = os.environ.get("DD_API_KEY")
    app_key = os.environ.get("DD_APP_KEY")
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key or not app_key:
        return MetricAnomalySummary(
            metric_name=metric_name,
            window_start=start,
            window_end=end,
            summary_text="Datadog credentials not configured",
        )

    config = Configuration()
    config.api_key["apiKeyAuth"] = api_key
    config.api_key["appKeyAuth"] = app_key
    config.host = DATADOG_API_HOST

    query_str = f"{aggregation.value}:{metric_name}"
    if dimensions:
        dim_parts = [f"{k}:{v}" for k, v in dimensions.items()]
        query_str = f"{query_str}{{{{{','.join(dim_parts)}}}}}"

    dd_request = DDQueryRequest(
        query=query_str,
        _from=int(start.timestamp()),
        to=int(end.timestamp()),
    )
    if interval_seconds:
        dd_request.interval = interval_seconds

    with ApiClient(config) as api_client:
        metrics_api = MetricsApi(api_client)
        raw_response = metrics_api.query_metrics(body=dd_request)

    response = normalize_datadog_response(raw_response)
    datapoints = response.datapoints

    summary = _detect_anomalies_and_trend(metric_name, start, end, datapoints)

    if openai_api_key:
        openai.api_key = openai_api_key
        summary.summary_text = _generate_summary_with_openai(
            metric_name, start, end, datapoints, summary
        )

    return summary


def _detect_anomalies_and_trend(
    metric_name: str,
    start: datetime,
    end: datetime,
    datapoints: list[tuple[datetime, float]],
) -> MetricAnomalySummary:
    if not datapoints:
        return MetricAnomalySummary(
            metric_name=metric_name,
            window_start=start,
            window_end=end,
            summary_text="No data points available",
        )

    values = [v for _, v in datapoints]
    n = len(values)
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / n
    stddev = variance**0.5

    anomaly_timestamps = []
    for ts, val in datapoints:
        if abs(val - mean) > 2 * stddev:
            anomaly_timestamps.append(ts)

    if n >= 2:
        x_vals = list(range(n))
        x_mean = sum(x_vals) / n
        slope_numerator = sum(
            (x - x_mean) * (y - mean) for x, (_, y) in zip(x_vals, datapoints)
        )
        slope_denominator = sum((x - x_mean) ** 2 for x in x_vals)
        trend_slope = (
            slope_numerator / slope_denominator if slope_denominator != 0 else 0.0
        )
    else:
        trend_slope = 0.0

    if trend_slope > 0.01:
        trend_direction = "increasing"
    elif trend_slope < -0.01:
        trend_direction = "decreasing"
    else:
        trend_direction = "stable"

    return MetricAnomalySummary(
        metric_name=metric_name,
        window_start=start,
        window_end=end,
        anomalies_detected=len(anomaly_timestamps),
        anomaly_timestamps=anomaly_timestamps,
        trend_direction=trend_direction,
        trend_slope=trend_slope,
    )


def _generate_summary_with_openai(
    metric_name: str,
    start: datetime,
    end: datetime,
    datapoints: list[tuple[datetime, float]],
    anomaly_summary: MetricAnomalySummary,
) -> str:
    sample_points = datapoints[:50]
    points_str = ", ".join(f"{ts.strftime('%H:%M')}={v:.2f}" for ts, v in sample_points)

    prompt = (
        f"Summarize the metric '{metric_name}' for the period {start.isoformat()} to {end.isoformat()}. "
        f"Recent values: [{points_str}]. "
        f"Trend direction: {anomaly_summary.trend_direction}. "
        f"Anomalies detected: {anomaly_summary.anomalies_detected}. "
        f"Provide a concise 2-3 sentence summary of the metric behavior."
    )

    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a metrics monitoring analyst. Provide concise summaries.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
            temperature=0.3,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return (
            f"Metric {metric_name} showed a {anomaly_summary.trend_direction} trend "
            f"with {anomaly_summary.anomalies_detected} anomalies detected."
        )

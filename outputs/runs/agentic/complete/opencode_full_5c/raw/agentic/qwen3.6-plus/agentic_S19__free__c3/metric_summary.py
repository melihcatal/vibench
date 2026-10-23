from datetime import datetime
from datadog_api_client import ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.metrics_query_request import MetricsQueryRequest
from openai import OpenAI
from observability_client import get_datadog_configuration, validate_time_window
from observability_models import (
    MetricSummary,
    MetricAnomaly,
    MetricSeries,
    detect_anomalies,
    normalize_datadog_series,
)


def summarize_metric_trends(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    dimensions: dict[str, str] | None = None,
    anomaly_sigma: float = 2.0,
) -> MetricSummary:
    config = get_datadog_configuration()
    validate_time_window(int(start_time.timestamp()), int(end_time.timestamp()))

    query_parts = [metric_name]
    if dimensions:
        for key, value in sorted(dimensions.items()):
            query_parts.append(f"{key}:{value}")
    query_string = " ".join(query_parts)

    body = MetricsQueryRequest(
        from_=int(start_time.timestamp()),
        to=int(end_time.timestamp()),
        query=query_string,
    )

    with ApiClient(config) as api_client:
        api_instance = MetricsApi(api_client)
        response = api_instance.query_metrics(body=body)

    all_series = []
    for raw_series in response.series:
        series = normalize_datadog_series(
            {
                "scope": raw_series.scope
                if hasattr(raw_series, "scope") and raw_series.scope
                else "",
                "pointlist": raw_series.pointlist
                if hasattr(raw_series, "pointlist")
                else [],
            },
            metric_name=metric_name,
            aggregation="avg",
        )
        all_series.append(series)

    if not all_series:
        return MetricSummary(
            metric_name=metric_name,
            period_start=start_time,
            period_end=end_time,
            overall_avg=0.0,
            overall_max=0.0,
            overall_min=0.0,
            trend_direction="unknown",
            anomalies=[],
            series=MetricSeries(
                metric_name=metric_name, aggregation="avg", dimensions={}, points=[]
            ),
        )

    primary_series = all_series[0]
    all_values = primary_series.values()

    if not all_values:
        return MetricSummary(
            metric_name=metric_name,
            period_start=start_time,
            period_end=end_time,
            overall_avg=0.0,
            overall_max=0.0,
            overall_min=0.0,
            trend_direction="unknown",
            anomalies=[],
            series=primary_series,
        )

    overall_avg = sum(all_values) / len(all_values)
    overall_max = max(all_values)
    overall_min = min(all_values)

    n = len(all_values)
    first_half_avg = sum(all_values[: n // 2]) / (n // 2) if n >= 2 else overall_avg
    second_half_avg = (
        sum(all_values[n // 2 :]) / (n - n // 2) if n >= 2 else overall_avg
    )

    if second_half_avg > first_half_avg * 1.05:
        trend_direction = "increasing"
    elif second_half_avg < first_half_avg * 0.95:
        trend_direction = "decreasing"
    else:
        trend_direction = "stable"

    anomalies = detect_anomalies(primary_series, sigma_threshold=anomaly_sigma)

    anomaly_descriptions = []
    for anomaly in anomalies:
        anomaly_descriptions.append(
            f"At {anomaly.timestamp.isoformat()}, value {anomaly.value:.2f} "
            f"deviated {anomaly.deviation:.1f} sigma from mean {anomaly.expected_value:.2f} "
            f"(severity: {anomaly.severity})"
        )

    summary_text = (
        f"Metric {metric_name} from {start_time.isoformat()} to {end_time.isoformat()}: "
        f"avg={overall_avg:.2f}, max={overall_max:.2f}, min={overall_min:.2f}, "
        f"trend={trend_direction}. "
        f"Found {len(anomalies)} anomalies. " + "; ".join(anomaly_descriptions)
    )

    openai_client = OpenAI()
    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a metrics analysis assistant. Provide a concise, professional summary of the metric trends and anomalies.",
            },
            {"role": "user", "content": summary_text},
        ],
        max_tokens=300,
    )

    refined_summary = completion.choices[0].message.content.strip()

    return MetricSummary(
        metric_name=metric_name,
        period_start=start_time,
        period_end=end_time,
        overall_avg=overall_avg,
        overall_max=overall_max,
        overall_min=overall_min,
        trend_direction=trend_direction,
        anomalies=anomalies,
        series=primary_series,
    )

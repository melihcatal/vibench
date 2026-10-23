from observability_client import get_generative_client
from observability_models import MetricData


def summarize_metrics(metric_data: list[MetricData]) -> str:
    """Summarizes metric trends using a generative model."""
    client = get_generative_client()

    if not metric_data:
        return "No metric data provided to summarize."

    prompt_lines = [
        "Please summarize the following metric data. "
        "Highlight any potential anomalies, upward or downward trends, or significant patterns."
    ]

    for series in metric_data:
        prompt_lines.append(f"\nMetric: {series.metric_name}")
        prompt_lines.append(f"Resource: {series.resource_labels}")
        if series.points:
            # Sort points to be safe, though they usually are
            sorted_points = sorted(series.points, key=lambda p: p.timestamp)
            prompt_lines.append("Data points (timestamp: value):")
            for point in sorted_points[:20]:  # Limit tokens
                prompt_lines.append(f"- {point.timestamp}: {point.value:.4f}")
        else:
            prompt_lines.append("No data points in this series.")

    prompt = "\n".join(prompt_lines)

    response = client.generate_content(prompt)

    return response.text


if __name__ == "__main__":
    # This is a mock example. In a real scenario, you would get this data from a query.
    mock_data = [
        MetricData(
            metric_name="custom.googleapis.com/user_satisfaction",
            resource_labels={"service": "frontend", "region": "us-central1"},
            points=[
                {"timestamp": "2023-10-27T10:00:00Z", "value": 0.98},
                {"timestamp": "2023-10-27T10:01:00Z", "value": 0.97},
                {"timestamp": "2023-10-27T10:02:00Z", "value": 0.75},  # Anomaly
                {"timestamp": "2023-10-27T10:03:00Z", "value": 0.96},
                {"timestamp": "2023-10-27T10:04:00Z", "value": 0.98},
            ],
        ),
        MetricData(
            metric_name="custom.googleapis.com/latency",
            resource_labels={"service": "backend", "region": "us-central1"},
            points=[
                {"timestamp": "2023-10-27T10:00:00Z", "value": 150.5},
                {"timestamp": "2023-10-27T10:01:00Z", "value": 155.2},
                {"timestamp": "2023-10-27T10:02:00Z", "value": 160.1},
                {"timestamp": "2023-10-27T10:03:00Z", "value": 165.8},  # Upward trend
                {"timestamp": "2023-10-27T10:04:00Z", "value": 170.3},
            ],
        ),
    ]
    summary = summarize_metrics(mock_data)
    print("--- Metric Summary ---")
    print(summary)

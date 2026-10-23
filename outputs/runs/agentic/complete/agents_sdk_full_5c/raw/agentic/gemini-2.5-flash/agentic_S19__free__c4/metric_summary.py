from observability_client import get_generative_model_client, configure_generative_model
from observability_models import MetricSummary
import os

def summarize_metric_trends(metric_data: list[dict], api_key: str, model_name: str = "gemini-pro") -> MetricSummary:
    configure_generative_model(api_key)
    model = get_generative_model_client(model_name)

    # Prepare a simple prompt for the generative model
    data_str = '
'.join([str(point) for point in metric_data])
    prompt = f"""Analyze the following metric data to identify trends or anomalies and provide a concise summary. Indicate if any significant anomalies are detected.

Metric Data:
{data_str}

Summary (Trend, Anomaly Detected (True/False), Summary Text):
"""

    response = model.generate_content(prompt)
    summary_text = response.text.strip()

    # Attempt to parse the summary text into a structured format
    # This is a very basic parsing and might need refinement for robustness
    trend = "Unknown"
    anomaly_detected = False
    parsed_summary = summary_text

    if "Anomaly Detected (True)" in summary_text:
        anomaly_detected = True
    elif "Anomaly Detected (False)" in summary_text:
        anomaly_detected = False

    if "Trend: " in summary_text:
        trend_start = summary_text.find("Trend: ") + len("Trend: ")
        trend_end = summary_text.find(",", trend_start)
        if trend_end != -1:
            trend = summary_text[trend_start:trend_end].strip()
        else:
            trend = summary_text[trend_start:].strip()

    return MetricSummary(
        metric_type="N/A",  # The actual metric type should ideally be passed in or inferred
        trend=trend,
        anomaly_detected=anomaly_detected,
        summary_text=parsed_summary,
    )

import os
from datetime import datetime, timedelta
from typing import Dict, Any
from observability_client import ObservabilityClient
from observability_models import TimeSeriesData
from query_metric_window import query_metric_window


def metric_summary(
    project_id: str,
    metric_type: str,
    end_time: datetime,
    start_time: datetime,
    threshold_percentage: float = 0.2,
) -> Dict[str, Any]:
    # Fetch time series data for the given metric and window
    time_series_data = query_metric_window(
        project_id=project_id,
        metric_type=metric_type,
        end_time=end_time,
        start_time=start_time,
    )

    if not time_series_data.points:
        return {"summary": f"No data found for metric {metric_type}"}

    values = [
        point["value"]
        for point in time_series_data.points
        if isinstance(point["value"], (int, float))
    ]

    if not values:
        return {"summary": f"No numeric data points for metric {metric_type}"}

    average_value = sum(values) / len(values)
    max_value = max(values)
    min_value = min(values)

    summary_message = f"Metric {metric_type} over {start_time} to {end_time}: "
    summary_message += (
        f"Average: {average_value:.2f}, Max: {max_value:.2f}, Min: {min_value:.2f}. "
    )

    # Simple anomaly detection: check for points significantly above/below average
    anomalies = []
    for point in time_series_data.points:
        value = point["value"]
        if isinstance(value, (int, float)):
            if value > average_value * (1 + threshold_percentage):
                anomalies.append(
                    f"High anomaly at {point['interval']['end_time']} (Value: {value:.2f})"
                )
            elif value < average_value * (1 - threshold_percentage):
                anomalies.append(
                    f"Low anomaly at {point['interval']['end_time']} (Value: {value:.2f})"
                )

    if anomalies:
        summary_message += "Potential anomalies detected: " + "; ".join(anomalies)
    else:
        summary_message += "No significant anomalies detected."

    return {
        "metric_type": metric_type,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "average_value": average_value,
        "max_value": max_value,
        "min_value": min_value,
        "anomalies": anomalies,
        "summary": summary_message,
    }

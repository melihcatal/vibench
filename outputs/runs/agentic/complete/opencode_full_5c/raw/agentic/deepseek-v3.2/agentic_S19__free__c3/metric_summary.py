import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2
import numpy as np


def summarize_metric_trends(metric_name, window_hours=24):
    """Summarize recent metric trends or anomalies."""
    client = monitoring_v3.MetricServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "my-project")
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval()
    now = datetime.utcnow()
    start_time = now - timedelta(hours=window_hours)

    start_timestamp = timestamp_pb2.Timestamp()
    start_timestamp.FromDatetime(start_time)
    end_timestamp = timestamp_pb2.Timestamp()
    end_timestamp.FromDatetime(now)

    interval.start_time = start_timestamp
    interval.end_time = end_timestamp

    filter_str = f'metric.type = "{metric_name}"'

    aggregation = monitoring_v3.Aggregation()
    aggregation.alignment_period = {"seconds": 300}
    aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
    aggregation.cross_series_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MEAN

    try:
        results = client.list_time_series(
            request={
                "name": project_name,
                "filter": filter_str,
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                "aggregation": aggregation,
            }
        )

        values = []
        timestamps = []

        for series in results:
            for point in series.points:
                value = (
                    point.value.double_value
                    if point.value.double_value
                    else point.value.int64_value
                )
                if value is not None:
                    values.append(value)
                    timestamps.append(point.interval.end_time.ToDatetime())

        if not values:
            return {
                "metric": metric_name,
                "window_hours": window_hours,
                "summary": "No data available",
                "has_anomalies": False,
            }

        values_array = np.array(values)

        mean = np.mean(values_array)
        std = np.std(values_array)
        min_val = np.min(values_array)
        max_val = np.max(values_array)

        anomalies = []
        if std > 0:
            z_scores = np.abs((values_array - mean) / std)
            anomaly_indices = np.where(z_scores > 2.5)[0]

            for idx in anomaly_indices:
                anomalies.append(
                    {
                        "timestamp": timestamps[idx].isoformat(),
                        "value": float(values_array[idx]),
                        "z_score": float(z_scores[idx]),
                        "deviation": float((values_array[idx] - mean) / mean * 100)
                        if mean != 0
                        else None,
                    }
                )

        trend = "stable"
        if len(values) >= 2:
            first_half = values_array[: len(values) // 2]
            second_half = values_array[len(values) // 2 :]

            if len(first_half) > 0 and len(second_half) > 0:
                mean_first = np.mean(first_half)
                mean_second = np.mean(second_half)

                if mean_second > mean_first * 1.2:
                    trend = "increasing"
                elif mean_second < mean_first * 0.8:
                    trend = "decreasing"

        summary = {
            "metric": metric_name,
            "window_hours": window_hours,
            "data_points": len(values),
            "mean": float(mean),
            "std_dev": float(std),
            "min": float(min_val),
            "max": float(max_val),
            "range": float(max_val - min_val),
            "trend": trend,
            "has_anomalies": len(anomalies) > 0,
            "anomaly_count": len(anomalies),
            "anomalies": anomalies[:10],
            "summary_text": f"Metric {metric_name} shows {trend} trend with mean {mean:.2f} ± {std:.2f}. "
            f"{len(anomalies)} potential anomalies detected."
            if len(anomalies) > 0
            else f"Metric {metric_name} shows {trend} trend with mean {mean:.2f} ± {std:.2f}. No anomalies detected.",
        }

        return summary

    except Exception as e:
        print(f"Error summarizing metric trends: {e}")
        return {
            "metric": metric_name,
            "window_hours": window_hours,
            "summary": f"Error: {str(e)}",
            "has_anomalies": False,
        }

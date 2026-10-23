from typing import Dict, List, Optional
import os
from datetime import datetime, timedelta
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from observability_client import ObservabilityClient
from observability_models import MetricSeries, AggregatedStats, calculate_stats


class MetricSummarizer:
    def __init__(self):
        self.mistral_client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
        self.observability_client = ObservabilityClient()

    def summarize_metric_trends(
        self,
        metric_type: str,
        hours: int = 24,
        filter_labels: Optional[Dict[str, str]] = None,
    ) -> str:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)

        from google.cloud import monitoring_v3
        from google.api import metric_service_v3

        client = self.observability_client.get_client()
        project_name = self.observability_client.get_project_name()

        interval = monitoring_v3.TimeInterval(end_time=end_time, start_time=start_time)

        metric_filter = f'metric.type="{metric_type}"'
        if filter_labels:
            filter_parts = self.observability_client.normalize_metric_filter(
                filter_labels
            )
            metric_filter += f" AND {filter_parts}"

        series = client.list_time_series(
            name=project_name,
            filter=metric_filter,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )

        metric_series = []
        for s in series:
            stats = calculate_stats(
                MetricSeries(metric_type=s.metric.type, points=[], unit=s.metric.unit)
            )
            for point in s.points:
                metric_series.append(
                    {
                        "timestamp": point.interval.end_time.ToDatetime().isoformat(),
                        "value": float(point.value.double_value),
                        "resource": dict(s.resource.labels),
                        "stats": {
                            "mean": stats.mean,
                            "min": stats.min,
                            "max": stats.max,
                        },
                    }
                )

        if not metric_series:
            return "No metric data available for the given time window."

        prompt = (
            "Summarize the following metric data and identify any trends or anomalies. "
            "Provide a concise summary in 2-3 sentences.\n"
            f"Metric Type: {metric_type}\n"
            f"Time Window: {start_time} to {end_time}\n"
            f"Data Points: {metric_series}"
        )

        response = self.mistral_client.chat(
            model="mistral-large-latest",
            messages=[ChatMessage(role="user", content=prompt)],
        )

        return response.choices[0].message.content

import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from google.cloud import monitoring_v3
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from observability_client import ObservabilityClient
from observability_models import MetricPoint, parse_metric_points


class MetricSummarizer:
    def __init__(self):
        self.monitoring_client = ObservabilityClient().client
        self.project_name = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}"
        self.mistral_client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    def summarize_metric_trends(self, metric_type: str, hours: int = 24) -> str:
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)

        interval = monitoring_v3.TimeInterval(end_time=end_time, start_time=start_time)

        metric_filter = f'metric.type="{metric_type}"'
        time_series_data = []
        for time_series in self.monitoring_client.list_time_series(
            name=self.project_name,
            filter=metric_filter,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        ):
            for point in time_series.points:
                time_series_data.append(
                    {
                        "timestamp": point.interval.end_time.ToDatetime().isoformat(),
                        "value": point.value.double_value,
                        "resource_labels": dict(time_series.resource.labels),
                        "metric_labels": dict(time_series.metric.labels),
                    }
                )

        if not time_series_data:
            return "No metric data available for the given time window."

        metric_points = parse_metric_points(time_series_data)
        context = self._build_context(metric_points)
        return self._generate_summary(context)

    def _build_context(self, metric_points: List[MetricPoint]) -> str:
        timestamps = [point.timestamp for point in metric_points]
        values = [point.value for point in metric_points]
        avg = sum(values) / len(values)
        min_val = min(values)
        max_val = max(values)

        return (
            f"Metric data from {timestamps[0]} to {timestamps[-1]}:\n"
            f"- Average value: {avg:.2f}\n"
            f"- Minimum value: {min_val:.2f}\n"
            f"- Maximum value: {max_val:.2f}\n"
            f"- Data points: {len(metric_points)}\n"
            f"- Sample values: {values[:5]}..."
        )

    def _generate_summary(self, context: str) -> str:
        messages = [
            ChatMessage(
                role="system",
                content="You are a metric analysis assistant. Provide a concise summary of the metric trends based on the provided data. "
                "Highlight any anomalies or notable patterns in 3-4 sentences.",
            ),
            ChatMessage(role="user", content=context),
        ]

        response = self.mistral_client.chat(
            model="mistral-large-latest", messages=messages
        )
        return response.choices[0].message.content

from openai import OpenAI
from observability_models import MetricStatsResponse, MetricComparisonResult
from typing import Union

class MetricSummarizer:
    def __init__(self):
        self.client = OpenAI(api_key="")  # Uses OPENAI_API_KEY from environment

    def summarize_metric_trends(self, metric_data: Union[MetricStatsResponse, MetricComparisonResult]) -> str:
        if isinstance(metric_data, MetricStatsResponse):
            prompt = (
                f"Summarize the following metric statistics for a {metric_data.metric_type} metric "
                f"over the last {metric_data.window_seconds} seconds:\n"
                f"- Count: {metric_data.count}\n"
                f"- Mean: {metric_data.mean:.2f}\n"
                f"- Min: {metric_data.min:.2f}\n"
                f"- Max: {metric_data.max:.2f}\n"
                "Provide a concise summary of trends or anomalies."
            )
        elif isinstance(metric_data, MetricComparisonResult):
            prompt = (
                f"Compare the following metric values for {metric_data.metric_type} "
                f"over the last {metric_data.window_seconds} seconds:\n"
                f"- Series A (labels: {metric_data.labels_a}): {metric_data.average_a:.2f}\n"
                f"- Series B (labels: {metric_data.labels_b}): {metric_data.average_b:.2f}\n"
                f"- Difference: {metric_data.difference:.2f}\n"
                "Provide a concise comparison and highlight anomalies."
            )
        else:
            raise ValueError("Unsupported metric data type")

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
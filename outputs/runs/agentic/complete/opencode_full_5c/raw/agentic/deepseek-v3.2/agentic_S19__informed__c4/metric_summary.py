import os
import json
from typing import Dict, List, Any, Optional
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
from observability_client import ObservabilityClient
from observability_models import MetricAggregationResult


class MetricSummarizer:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable must be set")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro")

    def summarize_metric_trends(
        self, metric_data: List[Dict[str, Any]], metric_name: str, time_window: str
    ) -> str:
        try:
            prompt = self._build_trend_summary_prompt(
                metric_data, metric_name, time_window
            )
            response = self.model.generate_content(prompt)
            return response.text
        except GoogleAPIError as e:
            print(f"Google Gemini API error: {e}")
            raise
        except Exception as e:
            print(f"Error summarizing metric trends: {e}")
            raise

    def detect_metric_anomalies(
        self, metric_data: List[Dict[str, Any]], metric_name: str
    ) -> Dict[str, Any]:
        try:
            prompt = self._build_anomaly_detection_prompt(metric_data, metric_name)
            response = self.model.generate_content(prompt)

            anomaly_result = {
                "summary": response.text,
                "has_anomalies": "anomaly" in response.text.lower()
                or "unusual" in response.text.lower(),
                "raw_response": response.text,
            }

            return anomaly_result
        except GoogleAPIError as e:
            print(f"Google Gemini API error: {e}")
            raise
        except Exception as e:
            print(f"Error detecting metric anomalies: {e}")
            raise

    def generate_metric_insights(
        self,
        aggregation_result: MetricAggregationResult,
        metric_name: str,
        context: str = "",
    ) -> str:
        try:
            prompt = self._build_insights_prompt(
                aggregation_result, metric_name, context
            )
            response = self.model.generate_content(prompt)
            return response.text
        except GoogleAPIError as e:
            print(f"Google Gemini API error: {e}")
            raise
        except Exception as e:
            print(f"Error generating metric insights: {e}")
            raise

    def _build_trend_summary_prompt(
        self, metric_data: List[Dict[str, Any]], metric_name: str, time_window: str
    ) -> str:
        data_summary = self._extract_data_summary(metric_data)

        prompt = f"""Analyze the following metric data and provide a concise summary of trends:
        
        Metric: {metric_name}
        Time Window: {time_window}
        
        Data Summary:
        {json.dumps(data_summary, indent=2)}
        
        Please provide:
        1. Overall trend direction (increasing, decreasing, stable, volatile)
        2. Key observations about the data pattern
        3. Any notable spikes, dips, or patterns
        4. Recommendations for monitoring or investigation if needed
        
        Keep the summary concise and actionable."""

        return prompt

    def _build_anomaly_detection_prompt(
        self, metric_data: List[Dict[str, Any]], metric_name: str
    ) -> str:
        data_summary = self._extract_data_summary(metric_data)

        prompt = f"""Analyze the following metric data for anomalies:
        
        Metric: {metric_name}
        
        Data Summary:
        {json.dumps(data_summary, indent=2)}
        
        Please:
        1. Identify any statistical anomalies or outliers
        2. Note any unusual patterns or deviations from expected behavior
        3. Flag potential issues that might require investigation
        4. Provide confidence level in anomaly detection
        
        If no anomalies are detected, state that clearly."""

        return prompt

    def _build_insights_prompt(
        self,
        aggregation_result: MetricAggregationResult,
        metric_name: str,
        context: str,
    ) -> str:
        agg_data = aggregation_result.to_dict()

        prompt = f"""Generate insights from the following metric aggregation:
        
        Metric: {metric_name}
        Context: {context if context else "General monitoring"}
        
        Aggregation Results:
        {json.dumps(agg_data, indent=2)}
        
        Please provide:
        1. Key performance indicators derived from these statistics
        2. Business or operational implications
        3. Recommendations for optimization or alerting
        4. Comparison to typical baseline if available
        
        Focus on actionable insights for operations teams."""

        return prompt

    def _extract_data_summary(
        self, metric_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        if not metric_data:
            return {"error": "No data available"}

        all_values = []
        timestamps = []

        for series in metric_data:
            for point in series.get("points", []):
                value = point.get("value")
                if isinstance(value, (int, float)):
                    all_values.append(value)
                    timestamps.append(point.get("timestamp"))

        if not all_values:
            return {"error": "No numeric values in data"}

        return {
            "data_points": len(all_values),
            "time_series_count": len(metric_data),
            "value_range": {
                "min": min(all_values),
                "max": max(all_values),
                "avg": sum(all_values) / len(all_values),
            },
            "time_range": {
                "start": min(timestamps) if timestamps else "unknown",
                "end": max(timestamps) if timestamps else "unknown",
            },
        }


def summarize_recent_metric_trends(metric_type: str, start_minutes: int) -> str:
    client = ObservabilityClient()
    summarizer = MetricSummarizer()

    filter_str = client.build_time_series_filter(metric_type)
    interval = client.parse_time_interval(start_minutes)

    request = monitoring_v3.ListTimeSeriesRequest(
        name=client.project_name,
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    time_series = client.client.list_time_series(request)
    normalized_data = client.normalize_metric_response(time_series)

    time_window = f"Last {start_minutes} minutes"
    return summarizer.summarize_metric_trends(normalized_data, metric_type, time_window)


def detect_service_anomalies(service_name: str, start_minutes: int) -> Dict[str, Any]:
    client = ObservabilityClient()
    summarizer = MetricSummarizer()

    metric_type = "run.googleapis.com/request_latencies"
    filter_str = f'resource.labels.service_name = "{service_name}"'
    full_filter = client.build_time_series_filter(metric_type, filter_str)

    interval = client.parse_time_interval(start_minutes)

    request = monitoring_v3.ListTimeSeriesRequest(
        name=client.project_name,
        filter=full_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    time_series = client.client.list_time_series(request)
    normalized_data = client.normalize_metric_response(time_series)

    return summarizer.detect_metric_anomalies(
        normalized_data, f"{service_name} latencies"
    )


def generate_cpu_insights(instance_id: str, start_minutes: int) -> str:
    from aggregate_metric_stats import get_aggregated_metric_stats

    metric_type = "compute.googleapis.com/instance/cpu/utilization"
    filter_str = f'resource.labels.instance_id = "{instance_id}"'

    client = ObservabilityClient()
    full_filter = client.build_time_series_filter(metric_type, filter_str)

    stats = get_aggregated_metric_stats(metric_type, start_minutes, 0, "REDUCE_MEAN")

    summarizer = MetricSummarizer()
    context = f"CPU utilization for instance {instance_id}"

    return summarizer.generate_metric_insights(stats, metric_type, context)

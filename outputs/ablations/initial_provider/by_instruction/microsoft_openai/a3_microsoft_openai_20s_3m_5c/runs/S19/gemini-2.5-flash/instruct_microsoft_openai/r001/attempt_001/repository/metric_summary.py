import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List

from observability_client import OpenAIMetricsClient
from observability_models import MetricQueryRequest, MetricQueryResponse, MetricDataPoint

def summarize_metric_trends(metric_data: MetricQueryResponse, custom_prompt: Optional[str] = None) -> str:
    """
    Summarizes recent metric trends or anomalies using OpenAI.

    Args:
        metric_data: A MetricQueryResponse object containing the metric data to summarize.
        custom_prompt: An optional custom prompt to guide the summary generation.

    Returns:
        A string containing the summary of metric trends or anomalies.
    """
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    client = OpenAIMetricsClient(api_key=openai_api_key)
    
    summary = client.summarize_metrics(metric_data, custom_prompt)
    return summary

if __name__ == '__main__':
    # Example usage: simulate some metric data to summarize
    end_time_example = datetime.utcnow()
    start_time_example = end_time_example - timedelta(hours=2)

    # Create a dummy MetricQueryResponse for demonstration
    # In a real scenario, this would come from a metric query function.
    sample_metric_data = MetricQueryResponse(
        metric_name="network_latency",
        unit="milliseconds",
        data_points=[
            MetricDataPoint(timestamp=start_time_example + timedelta(minutes=10), value=25.0, dimensions={"region": "us-west-1"}),
            MetricDataPoint(timestamp=start_time_example + timedelta(minutes=20), value=28.0, dimensions={"region": "us-west-1"}),
            MetricDataPoint(timestamp=start_time_example + timedelta(minutes=30), value=32.0, dimensions={"region": "us-west-1"}),
            MetricDataPoint(timestamp=start_time_example + timedelta(minutes=40), value=150.0, dimensions={"region": "us-west-1"}), # Anomaly
            MetricDataPoint(timestamp=start_time_example + timedelta(minutes=50), value=30.0, dimensions={"region": "us-west-1"}),
            MetricDataPoint(timestamp=start_time_example + timedelta(minutes=60), value=27.0, dimensions={"region": "us-west-1"}),
            MetricDataPoint(timestamp=start_time_example + timedelta(minutes=70), value=29.0, dimensions={"region": "us-west-1"}),
            MetricDataPoint(timestamp=start_time_example + timedelta(minutes=80), value=31.0, dimensions={"region": "us-west-1"}),
            MetricDataPoint(timestamp=start_time_example + timedelta(minutes=90), value=26.0, dimensions={"region": "us-west-1"}),
            MetricDataPoint(timestamp=end_time_example, value=28.0, dimensions={"region": "us-west-1"})
        ]
    )

    print(f"Summarizing metric trends for '{sample_metric_data.metric_name}'...")
    try:
        summary_text = summarize_metric_trends(sample_metric_data)
        print("\nMetric Summary:")
        print(summary_text)

        print("\nSummarizing with a custom prompt:")
        custom_summary_text = summarize_metric_trends(
            sample_metric_data,
            custom_prompt="Provide a detailed technical analysis of the network latency data, focusing on the potential root cause of any spikes."
        )
        print(custom_summary_text)

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

import os
import json
from openai import OpenAI
from observability_models import TimeSeries, MetricDataPoint

def summarize_metric_data(time_series: TimeSeries) -> str:
    """
    Summarizes metric data trends using OpenAI's GPT model.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    client = OpenAI(api_key=api_key)
    
    # Prepare data for the prompt
    points_str = json.dumps([
        {"timestamp": p.timestamp, "value": p.value} for p in time_series.points
    ], indent=2)

    prompt = f"""
    The following is a series of metric data points for the metric '{time_series.metric_name}'
    for the resource with labels {time_series.resource_labels}.
    Please provide a brief, human-readable summary of the trend.
    Mention any notable spikes, dips, or periods of stability.

    Data:
    {points_str}
    """

    response = client.chat.completions.create(
        model="gpt-4o",  # Provider-specific model identifier
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes monitoring data."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=150,
    )
    
    summary = response.choices[0].message.content
    return summary.strip()

if __name__ == '__main__':
    # Example usage with mock data
    mock_series = TimeSeries(
        metric_name="example.metric/cpu/usage",
        resource_labels={"host": "server-123", "zone": "us-central1-a"},
        points=[
            MetricDataPoint(timestamp="2023-10-27T10:00:00Z", value=0.12),
            MetricDataPoint(timestamp="2023-10-27T10:01:00Z", value=0.15),
            MetricDataPoint(timestamp="2023-10-27T10:02:00Z", value=0.14),
            MetricDataPoint(timestamp="2023-10-27T10:03:00Z", value=0.88), # A spike
            MetricDataPoint(timestamp="2023-10-27T10:04:00Z", value=0.16),
        ]
    )
    try:
        trend_summary = summarize_metric_data(mock_series)
        print("--- Metric Trend Summary ---")
        print(trend_summary)
    except (ValueError, ImportError) as e:
        print(f"Error: {e}")

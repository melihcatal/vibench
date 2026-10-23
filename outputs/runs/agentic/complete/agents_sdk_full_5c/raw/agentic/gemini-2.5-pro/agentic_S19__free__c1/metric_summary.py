
import os
import json
from openai import OpenAI

from observability_models import MetricSeries, TimeSeriesPoint


def summarize_metric_data(series: MetricSeries) -> str:
    """
    Uses OpenAI's GPT model to generate a human-readable summary of metric data.

    Args:
        series: A MetricSeries object containing time series data.

    Returns:
        A string containing the summary.
    """
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI()

    # Prepare the data for the prompt
    points_json = json.dumps(
        [{"t": p.timestamp, "v": p.value} for p in series.points], 
        indent=2
    )
    
    prompt = f"""
    The following JSON data represents a time series for the metric '{series.name}'
    with resource labels {json.dumps(series.resource_labels)}.
    
    Data:
    {points_json}

    Please provide a brief, human-readable summary of this data.
    Identify any notable trends, peaks, or troughs. For example, is the value
    generally increasing, decreasing, or stable?
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful monitoring assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating summary: {e}"


if __name__ == "__main__":
    # Create some sample data for demonstration
    sample_series = MetricSeries(
        name="compute.googleapis.com/instance/cpu/utilization",
        resource_labels={"project_id": "demo-project", "instance_id": "12345", "zone": "us-west1-a"},
        points=[
            TimeSeriesPoint(timestamp="2023-10-27T10:00:00Z", value=0.12),
            TimeSeriesPoint(timestamp="2023-10-27T10:05:00Z", value=0.15),
            TimeSeriesPoint(timestamp="2023-10-27T10:10:00Z", value=0.14),
            TimeSeriesPoint(timestamp="2023-10-27T10:15:00Z", value=0.58),
            TimeSeriesPoint(timestamp="2023-10-27T10:20:00Z", value=0.61),
            TimeSeriesPoint(timestamp="2023-10-27T10:25:00Z", value=0.22),
        ],
    )

    summary = summarize_metric_data(sample_series)
    print("--- Metric Summary ---")
    print(summary)
    print("----------------------")


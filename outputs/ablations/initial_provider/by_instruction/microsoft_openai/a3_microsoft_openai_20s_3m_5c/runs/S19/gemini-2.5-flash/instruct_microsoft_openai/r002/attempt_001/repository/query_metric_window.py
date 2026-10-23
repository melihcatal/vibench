from observability_client import ObservabilityClient
from observability_models import MetricQueryResult, MetricDatapoint
from typing import List
import datetime

def query_metric_window(
    metric_name: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
) -> MetricQueryResult:
    """Queries recent datapoints for a named metric over a time window using OpenAI to simulate data.

    Args:
        metric_name: The name of the metric to query.
        start_time: The start of the time window.
        end_time: The end of the time window.

    Returns:
        A MetricQueryResult containing simulated datapoints and a summary from OpenAI.
    """
    client = ObservabilityClient().get_openai_client()
    
    # Simulate generating metric data and a summary using OpenAI
    prompt = (
        f"Simulate recent datapoints for a metric named '{metric_name}' "
        f"between {start_time.isoformat()} and {end_time.isoformat()}. "
        f"Provide a brief summary of the trend. "
        f"Generate 5 hypothetical datapoints within this window. "
        f"Return in a JSON-like format with 'summary' and 'datapoints' (timestamp, value)."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using a concrete OpenAI model
            messages=[
                {"role": "system", "content": "You are a helpful assistant that simulates metric data trends."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        openai_output = response.choices[0].message.content.strip()
        
        # In a real scenario, we would parse this more robustly.
        # For this simulation, we'll try to extract a summary and some placeholder data.
        summary = "Simulated trend: " + openai_output # Simple extraction for demonstration
        
        # Placeholder for simulated datapoints - in a real app, this would be parsed from OpenAI's output
        # or directly from a metrics backend.
        simulated_datapoints: List[MetricDatapoint] = []
        current_time = start_time
        time_delta = (end_time - start_time) / 5
        for i in range(5):
            simulated_datapoints.append(MetricDatapoint(
                timestamp=(current_time + i * time_delta).isoformat(),
                value=float(i * 10 + 50) # Example placeholder values
            ))

        return MetricQueryResult(
            metric_name=metric_name,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            datapoints=simulated_datapoints
        )
    except Exception as e:
        # Handle API errors or other exceptions
        print(f"Error querying OpenAI: {e}")
        return MetricQueryResult(
            metric_name=metric_name,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            datapoints=[],
        )

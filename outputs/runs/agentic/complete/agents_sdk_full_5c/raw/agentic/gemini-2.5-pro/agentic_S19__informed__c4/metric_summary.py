import os
import json
from typing import Dict, Any
import anthropic

def summarize_metric_trends(metric_data: Dict[str, Any]) -> str:
    """
    Uses an LLM to summarize recent metric trends or anomalies.

    Args:
        metric_data: A dictionary representing metric data, e.g., from a monitoring query.

    Returns:
        A string containing a summary of the metric data.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    try:
        client = anthropic.Anthropic(api_key=api_key)
    except Exception as e:
        return f"Error creating Anthropic client: {e}"

    # Prepare the data for the prompt
    prompt_data = json.dumps(metric_data, indent=2)
    prompt = f"""
The following JSON data represents time-series metric data for CPU utilization. 
Please analyze this data for any notable trends, spikes, or anomalies and provide a brief, human-readable summary.

Data:
{prompt_data}

Summary:
"""

    try:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=250,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        summary = message.content[0].text if message.content else "No summary generated."
        return summary
    except Exception as e:
        return f"An error occurred while calling the Anthropic API: {e}"

if __name__ == '__main__':
    # Example metric data
    example_data = {
        "metric": "cpu_utilization_percent",
        "resource": "api-server-prod-1",
        "time_window": "30 minutes",
        "data_points": [
            {"timestamp": "2023-10-27T10:00:00Z", "value": 15.2},
            {"timestamp": "2023-10-27T10:05:00Z", "value": 16.1},
            {"timestamp": "2023-10-27T10:10:00Z", "value": 15.5},
            {"timestamp": "2023-10-27T10:15:00Z", "value": 45.8},
            {"timestamp": "2023-10-27T10:20:00Z", "value": 47.2},
            {"timestamp": "2023-10-27T10:25:00Z", "value": 15.9},
        ]
    }
    
    summary_text = summarize_metric_trends(example_data)
    print("--- Metric Summary ---")
    print(summary_text)

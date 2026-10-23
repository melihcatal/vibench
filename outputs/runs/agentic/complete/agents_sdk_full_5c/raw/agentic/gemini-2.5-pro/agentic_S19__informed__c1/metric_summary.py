import os
import json
from typing import List, Dict, Any
import openai

def summarize_metric_trends(metric_name: str, data_points: List[Dict[str, Any]]) -> str:
    """
    Summarize recent metric trends or anomalies using an LLM.

    Args:
        metric_name: The name of the metric being summarized.
        data_points: A list of data points, where each point is a dictionary
                     (e.g., {'timestamp': '...', 'value': ...}).

    Returns:
        A natural language summary of the metric trends.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = openai.OpenAI(api_key=api_key)

    # Convert data points to a string format for the prompt
    data_str = json.dumps(data_points, indent=2)

    prompt = f"""
    The following data represents recent measurements for the metric "{metric_name}":

    {data_str}

    Please provide a concise, one-paragraph summary of this data. Highlight any notable trends,
    spikes, or anomalies. Do not start with "The data shows" or similar phrases.
    Start directly with the analysis.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a monitoring and observability expert."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=150,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "No summary could be generated."
    except openai.APIError as e:
        return f"Error from OpenAI API: {e}"

if __name__ == '__main__':
    # This is an example and will not be executed in the test environment.
    sample_metric_name = "api.service.com/request_latency_p99"
    sample_data = [
        {"timestamp": "2023-10-27T10:00:00Z", "value": 120},
        {"timestamp": "2023-10-27T10:05:00Z", "value": 125},
        {"timestamp": "2023-10-27T10:10:00Z", "value": 130},
        {"timestamp": "2023-10-27T10:15:00Z", "value": 250}, # Spike
        {"timestamp": "2023-10-27T10:20:00Z", "value": 135},
        {"timestamp": "2023-10-27T10:25:00Z", "value": 132},
    ]

    try:
        trend_summary = summarize_metric_trends(sample_metric_name, sample_data)
        print(f"Metric: {sample_metric_name}")
        print(f"Summary: {trend_summary}")
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


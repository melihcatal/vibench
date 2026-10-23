import os
import openai
import json
from typing import List, Dict, Any

# Ensure the OpenAI API key is set
if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

def summarize_metric_data(metric_name: str, data_points: List[Dict[str, Any]]) -> str:
    """
    Uses an LLM to summarize recent metric trends or anomalies.

    Args:
        metric_name: The name of the metric being summarized.
        data_points: A list of data points, each a dictionary with 'timestamp' and 'value'.

    Returns:
        A text summary of the metric data.
    """
    client = openai.OpenAI()

    # Convert data points to a more compact string representation for the prompt
    data_str = json.dumps(data_points, indent=2)

    prompt = f"""
    Analyze the following time series data for the metric '{metric_name}' and provide a brief summary.
    Focus on the overall trend (e.g., increasing, decreasing, stable) and highlight any significant spikes, dips, or anomalies.

    Data:
    {data_str}

    Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes monitoring data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=200,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "No summary could be generated."
    except openai.APIError as e:
        return f"Error from OpenAI API: {e}"


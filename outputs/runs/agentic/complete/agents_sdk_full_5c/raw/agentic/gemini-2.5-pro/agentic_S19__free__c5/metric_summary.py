
import os
import json
from openai import OpenAI
from typing import List, Dict, Any

def summarize_metric_data(metric_name: str, data_points: List[Dict[str, Any]]) -> str:
    """
    Summarizes metric data to identify trends or anomalies using OpenAI.

    Args:
        metric_name: The name of the metric being summarized.
        data_points: A list of data points, each a dict with 'timestamp' and 'value'.

    Returns:
        A natural language summary of the metric data.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    client = OpenAI(api_key=api_key)
    
    # Prune data if too long to fit in prompt
    if len(data_points) > 100:
        data_points = data_points[-100:]

    prompt = f"""
    The following is a series of data points for the metric '{metric_name}'.
    Please provide a brief, one-paragraph summary of this data.
    Focus on identifying any significant trends, anomalies, spikes, or dips.
    
    Data:
    {json.dumps(data_points)}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes monitoring data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=200,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {e}"

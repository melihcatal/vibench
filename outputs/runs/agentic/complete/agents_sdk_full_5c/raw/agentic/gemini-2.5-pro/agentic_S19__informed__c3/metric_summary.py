import os
import json
from openai import OpenAI
from typing import List, Dict, Any

def summarize_metric_data(metric_data: List[Dict[str, Any]], metric_name: str) -> str:
    """
    Summarizes recent metric trends or anomalies using an LLM.

    :param metric_data: A list of time series data points.
    :param metric_name: The name of the metric being summarized.
    :return: A natural language summary of the metric data.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if not metric_data:
        return "No metric data available to summarize."

    # Serialize the data for the prompt
    data_str = json.dumps(metric_data, indent=2)

    prompt = f"""
    You are a monitoring and observability expert.
    Analyze the following time series data for the metric '{metric_name}' and provide a concise summary.
    Highlight any significant trends, spikes, dips, or anomalous patterns.

    Metric Data:
    {data_str}

    Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert system that analyzes time series data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=250,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate a summary."
    except Exception as e:
        return f"An error occurred while generating the summary: {e}"

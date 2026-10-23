import os
import json
from openai import OpenAI
from typing import List, Dict, Any

# Provider: OpenAI
# Task: Summarize recent metric trends or anomalies

def summarize_metric_data(time_series_data: List[Dict[str, Any]], model_id: str = "gpt-4o") -> str:
    """
    Uses OpenAI's GPT model to generate a human-readable summary of metric data.
    
    Args:
        time_series_data: A list of dictionaries representing time series data points.
        model_id: The OpenAI model to use for summarization.

    Returns:
        A string containing the summary.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
        
    client = OpenAI(api_key=api_key)

    # Prune data if it's too long to fit in the prompt
    if len(time_series_data) > 50:
        time_series_data = time_series_data[-50:]

    prompt_content = f"""
    The following is a JSON object representing time series data for a single metric.
    Each object in the list contains a 'timestamp' and a 'value'.
    Please analyze this data and provide a brief, human-readable summary.
    Focus on identifying any significant trends, anomalies, spikes, or dips.

    Data:
    {json.dumps(time_series_data, indent=2)}

    Summary:
    """

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes monitoring data."},
                {"role": "user", "content": prompt_content},
            ],
            temperature=0.5,
            max_tokens=150,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "No summary could be generated."
    except Exception as e:
        return f"An error occurred while communicating with the OpenAI API: {e}"

if __name__ == '__main__':
    # Example usage with dummy data
    if not os.getenv("OPENAI_API_KEY"):
        print("Skipping example run: OPENAI_API_KEY is not set.")
    else:
        print("Summarizing example metric data...")
        example_data = [
            {'timestamp': '2023-10-27T10:00:00Z', 'value': 0.12},
            {'timestamp': '2023-10-27T10:05:00Z', 'value': 0.11},
            {'timestamp': '2023-10-27T10:10:00Z', 'value': 0.13},
            {'timestamp': '2023-10-27T10:15:00Z', 'value': 0.58}, # Anomaly/Spike
            {'timestamp': '2023-10-27T10:20:00Z', 'value': 0.14},
            {'timestamp': '2023-10-27T10:25:00Z', 'value': 0.12},
        ]
        
        summary_text = summarize_metric_data(example_data)
        print("\n--- Generated Summary ---")
        print(summary_text)
        print("-------------------------")

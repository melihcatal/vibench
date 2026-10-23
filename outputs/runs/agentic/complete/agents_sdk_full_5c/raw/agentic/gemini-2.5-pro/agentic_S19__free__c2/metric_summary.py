import os
from typing import List, Dict, Any
from observability_client import ClientFactory
from observability_models import MetricData


def summarize_metric_data(metric_data: List[MetricData], metric_name: str) -> str:
    """
    Summarizes recent metric trends or anomalies using a generative AI model.

    Args:
        metric_data: A list of MetricData objects.
        metric_name: The name of the metric being analyzed.

    Returns:
        A natural language summary of the metric data.
    """
    client = ClientFactory.get_openai_client()

    if not metric_data:
        return "No metric data provided for summarization."

    # Flatten the data points for the prompt
    prompt_data = ""
    for series in metric_data:
        dimensions_str = ", ".join(f"{k}={v}" for k, v in series.dimensions.items())
        prompt_data += f"Series ({dimensions_str}):\n"
        for point in series.points:
            prompt_data += f"  Timestamp: {point.timestamp}, Value: {point.value:.2f}\n"

    prompt = f"""
    You are an expert monitoring analyst. Analyze the following time series data for the metric '{metric_name}'
    and provide a brief, human-readable summary. Focus on identifying any significant trends, anomalies,
    spikes, or flatlines.

    Data:
    {prompt_data}

    Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Using a specific OpenAI model
            messages=[
                {"role": "system", "content": "You are a helpful monitoring analyst."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=200,
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        return f"Error generating summary: {e}"

# Example usage would need metric data from another function and an OpenAI API key.
# if __name__ == '__main__':
#     if os.environ.get("OPENAI_API_KEY"):
#         # Create some dummy data for demonstration
#         dummy_data = [
#             MetricData(
#                 metric_name="cpu.utilization",
#                 points=[
#                     {"timestamp": 1672531200, "value": 10.5},
#                     {"timestamp": 1672531500, "value": 11.0},
#                     {"timestamp": 1672531800, "value": 80.2}, # Anomaly
#                     {"timestamp": 1672532100, "value": 10.8},
#                 ],
#                 dimensions={"host": "server-1"}
#             )
#         ]
#         summary_text = summarize_metric_data(dummy_data, "CPU Utilization")
#         print(summary_text)
#     else:
#         print("OPENAI_API_KEY environment variable not set.")

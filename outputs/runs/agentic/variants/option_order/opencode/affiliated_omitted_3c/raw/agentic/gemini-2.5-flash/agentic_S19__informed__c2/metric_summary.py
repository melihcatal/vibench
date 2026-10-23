import os
from typing import List, Dict, Any
import openai  # OpenAI SDK

# Ensure the OpenAI API key is set in the environment
openai.api_key = os.environ.get("OPENAI_API_KEY")


def summarize_metric_trends(
    metric_data: List[Dict[str, Any]], additional_context: str = ""
) -> str:
    """Summarizes recent metric trends or anomalies using OpenAI's GPT models.

    Args:
        metric_data (List[Dict[str, Any]]): A list of dictionaries, where each dictionary represents
                                           a metric data point or aggregated statistic.
                                           Example: [{'timestamp': '...', 'value': '...', 'unit': '...'}]
        additional_context (str, optional): Any additional context or specific questions to guide the summary.

    Returns:
        str: A summary of the metric trends or anomalies.
    """
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    # Convert metric_data to a string format suitable for the LLM
    metric_data_str = "\n".join([str(item) for item in metric_data])

    prompt = f"""
    Analyze the following metric data and provide a concise summary of recent trends or anomalies. 
    {additional_context}

    Metric Data:
    {metric_data_str}

    Summary:
    """

    try:
        # Using a common chat model, e.g., gpt-3.5-turbo or gpt-4
        # Model identification: gpt-3.5-turbo
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that analyzes metric data.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
        )
        return response.choices[0].message["content"].strip()
    except openai.error.OpenAIError as e:
        return f"Error summarizing metrics: {e}"

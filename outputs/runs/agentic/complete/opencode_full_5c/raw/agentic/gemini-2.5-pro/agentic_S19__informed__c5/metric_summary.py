import os
import json
import google.generativeai as genai


def summarize_metric_data(metric_data_json: str) -> str:
    """
    Summarizes metric data using the Google Gemini API.

    Args:
        metric_data_json: A JSON string of metric data.

    Returns:
        A string containing a summary of the metric data.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    Analyze the following metric data and provide a brief summary of trends,
    anomalies, or key observations. The data is in JSON format.
    
    Data:
    {metric_data_json}
    
    Summary:
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while generating summary: {e}"


if __name__ == "__main__":
    # Example metric data
    example_data = [
        {
            "metric_labels": {"instance_name": "instance-1"},
            "points": [{"timestamp": "2023-10-27T10:00:00Z", "value": 0.5}],
        },
        {
            "metric_labels": {"instance_name": "instance-1"},
            "points": [{"timestamp": "2023-10-27T10:05:00Z", "value": 0.9}],
        },
        {
            "metric_labels": {"instance_name": "instance-2"},
            "points": [{"timestamp": "2023-10-27T10:00:00Z", "value": 0.2}],
        },
        {
            "metric_labels": {"instance_name": "instance-2"},
            "points": [{"timestamp": "2023-10-27T10:05:00Z", "value": 0.25}],
        },
    ]

    summary = summarize_metric_data(json.dumps(example_data))
    print(summary)

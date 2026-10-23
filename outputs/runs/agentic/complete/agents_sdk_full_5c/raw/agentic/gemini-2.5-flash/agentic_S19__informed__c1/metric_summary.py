
import os
import google.generativeai as genai

def summarize_metric_trends(metric_data: list, prompt_prefix: str = "Summarize the following metric data and identify any significant trends or anomalies:") -> str:
    """
    Summarizes recent metric trends or anomalies using the Google Gemini API.
    metric_data is expected to be a list of dictionaries, e.g., from observability_models.normalize_list_time_series_response.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return "Error: GOOGLE_API_KEY environment variable not set."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    # Convert metric data to a more readable string for the LLM
    data_str = "\n".join([str(point) for point in metric_data])
    full_prompt = f"{prompt_prefix}\n\n{data_str}"

    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"

if __name__ == "__main__":
    # Example usage (replace with actual metric data)
    example_metric_data = [
        {"timestamp": "2023-10-27T10:00:00Z", "value": 0.1, "resource_labels": {"instance_name": "test-instance-1"}},
        {"timestamp": "2023-10-27T10:01:00Z", "value": 0.12, "resource_labels": {"instance_name": "test-instance-1"}},
        {"timestamp": "2023-10-27T10:02:00Z", "value": 0.8, "resource_labels": {"instance_name": "test-instance-1"}},
        {"timestamp": "2023-10-27T10:03:00Z", "value": 0.85, "resource_labels": {"instance_name": "test-instance-1"}},
        {"timestamp": "2023-10-27T10:04:00Z", "value": 0.15, "resource_labels": {"instance_name": "test-instance-1"}},
    ]
    summary = summarize_metric_trends(example_metric_data)
    print("Metric Summary:")
    print(summary)

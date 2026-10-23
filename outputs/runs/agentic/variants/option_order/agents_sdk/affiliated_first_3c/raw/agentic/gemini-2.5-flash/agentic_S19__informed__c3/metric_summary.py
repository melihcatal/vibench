import os
import google.generativeai as genai

def summarize_metric_trends(metric_data: str, model_name: str = "gemini-pro") -> str:
    """Summarizes recent metric trends or anomalies using the Google Gemini API.

    Args:
        metric_data: A string representation of the metric data (e.g., JSON, or a descriptive text).
        model_name: The Gemini model to use for summarization (default: 'gemini-pro').

    Returns:
        A string containing the summary of the metric trends or anomalies.
    """
    # Ensure GOOGLE_API_KEY is set in environment variables
    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it to use the Gemini API.")

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

    model = genai.GenerativeModel(model_name)

    prompt = f"""Analyze the following metric data and summarize any notable trends, anomalies, or key observations. Focus on changes over time, significant peaks or dips, and potential implications.

Metric Data:
{metric_data}

Summary:"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating summary: {e}"

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable to be set)
    # # In a real scenario, metric_data would come from your monitoring system
    # sample_metric_data = """
    # CPU Utilization for server 'web-01' over the last hour:
    # 10:00:00 - 45%
    # 10:05:00 - 48%
    # 10:10:00 - 52%
    # 10:15:00 - 55%
    # 10:20:00 - 90% (spike!)
    # 10:25:00 - 88%
    # 10:30:00 - 85%
    # 10:35:00 - 60%
    # 10:40:00 - 55%
    # 10:45:00 - 53%
    # 10:50:00 - 50%
    # 10:55:00 - 47%
    # """

    # try:
    #     summary = summarize_metric_trends(sample_metric_data)
    #     print("\n--- Metric Summary ---")
    #     print(summary)
    # except ValueError as e:
    #     print(e)
    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
    pass

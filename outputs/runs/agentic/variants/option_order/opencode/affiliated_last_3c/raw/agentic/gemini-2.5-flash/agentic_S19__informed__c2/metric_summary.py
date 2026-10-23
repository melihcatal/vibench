import os
import google.generativeai as genai


def summarize_metric_trends(metric_data_description: str) -> str:
    """Summarizes recent metric trends or anomalies using the Google Gemini API."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-pro")  # Using a concrete model family

    prompt = f"""Analyze the following metric data description and summarize any significant trends or anomalies. 
    
    Metric Data: {metric_data_description}
    
    Summary:"""

    response = model.generate_content(prompt)
    return response.text


# Example usage (assuming GOOGLE_API_KEY is set and you have a metric_data_description string)
# if __name__ == "__main__":
#     example_metric_description = "CPU utilization for instance-1 shows a steady increase from 20% to 80% over the last hour, with a sharp spike to 95% at 10:30 AM UTC."
#     summary = summarize_metric_trends(example_metric_description)
#     print(summary)

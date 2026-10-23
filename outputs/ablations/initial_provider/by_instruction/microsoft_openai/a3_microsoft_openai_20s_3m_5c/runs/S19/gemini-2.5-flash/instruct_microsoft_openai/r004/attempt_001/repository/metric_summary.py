import os
from datetime import datetime
from typing import List
from observability_client import ObservabilityClient
from observability_models import MetricDataPoint, MetricSummary

def summarize_metric_trends_or_anomalies(
    metric_name: str,
    data_points: List[MetricDataPoint]
) -> MetricSummary:
    """
    Summarize recent metric trends or anomalies using Google Generative AI (Gemini).
    """
    google_gemini_api_key = os.environ.get("GOOGLE_GEMINI_API_KEY")
    if not google_gemini_api_key:
        raise ValueError("GOOGLE_GEMINI_API_KEY environment variable not set.")

    # OpenAI API Key is not directly used for this file but passed for client initialization consistency.
    dummy_openai_api_key = os.environ.get("OPENAI_API_KEY", "dummy_key") 

    client = ObservabilityClient(
        openai_api_key=dummy_openai_api_key,
        google_gemini_api_key=google_gemini_api_key
    )

    summary_response = client.summarize_metric_trends_gemini(
        metric_name=metric_name,
        data_points=data_points
    )
    return summary_response

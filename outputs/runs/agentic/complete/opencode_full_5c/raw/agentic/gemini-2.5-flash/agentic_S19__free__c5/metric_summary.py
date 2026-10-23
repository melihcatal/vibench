import os
from observability_client import get_generative_model

def summarize_metric_trends(metric_data: str):
    """Summarize recent metric trends or anomalies using a generative AI model."""
    model = get_generative_model(model_name="gemini-pro")
    prompt = (
        "Analyze the following metric data and provide a concise summary of recent trends or anomalies. "
        "Highlight any significant changes, spikes, dips, or patterns observed:

"
        f"{metric_data}"
    )
    response = model.generate_content(prompt)
    return response.text

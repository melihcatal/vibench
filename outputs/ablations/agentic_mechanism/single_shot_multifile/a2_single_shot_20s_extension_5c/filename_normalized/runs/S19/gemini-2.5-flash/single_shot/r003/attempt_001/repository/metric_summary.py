import os
import openai
from observability_models import MetricSeries

def summarize_metric_trends(metric_series_data: list[MetricSeries], context: str = "") -> str:
    openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Format metric data into a string for the LLM
    formatted_data = []
    for series in metric_series_data:
        series_str = f"Resource Labels: {series.resource_labels}, Metric Labels: {series.metric_labels}\n"
        for dp in series.datapoints:
            series_str += f"  Timestamp: {dp.timestamp}, Value: {dp.value}\n"
        formatted_data.append(series_str)

    prompt_text = (
        f"Analyze the following metric time series data and summarize any noticeable trends, anomalies, "
        f"or significant changes. Also consider this context: {context}\n\n"
        f"Metric Data:\n{os.linesep.join(formatted_data)}\n\nSummary:"
    )

    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert at analyzing time-series metric data and identifying trends or anomalies."},
            {"role": "user", "content": prompt_text}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content
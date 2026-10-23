import json
from typing import List
from observability_client import ObservabilityClient
from observability_models import MetricDatapoint, MetricQueryResult

def summarize_metric_trends(metric_name: str, datapoints: List[MetricDatapoint]) -> str:
    client = ObservabilityClient()

    # Prepare data for OpenAI
    data_for_ai = [
        {"timestamp": dp.timestamp, "value": dp.value, "dimensions": dp.dimensions}
        for dp in datapoints
    ]

    prompt = f"Given the following metric data for '{metric_name}': {json.dumps(data_for_ai)}\n\nSummarize the recent trends, identify any anomalies, and provide insights. Focus on the overall pattern, significant changes, and potential causes or implications. Keep the summary concise, under 200 words."

    response = client.openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes metric data and identifies trends/anomalies."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )

    return response.choices[0].message.content.strip()

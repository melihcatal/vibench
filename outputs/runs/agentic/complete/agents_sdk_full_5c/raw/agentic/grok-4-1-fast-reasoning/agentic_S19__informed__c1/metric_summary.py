import openai
import os
from typing import List
from observability_models import MetricDatapoint

def metric_summary(
    datapoints: List[MetricDatapoint],
    metric_name: str
) -> str:
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    data_str = ', '.join([f"{dp.timestamp}: {dp.value}" for dp in datapoints])
    prompt = f"""
    Summarize recent trends or anomalies for the metric '{metric_name}'.
    Datapoints: {data_str}
    
    Provide a concise summary highlighting key trends, peaks, drops, or anomalies.
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content

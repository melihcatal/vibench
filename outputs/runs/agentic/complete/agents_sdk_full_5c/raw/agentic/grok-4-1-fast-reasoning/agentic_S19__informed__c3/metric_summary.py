import openai
import os
from observability_client import cloudwatch_client, get_time_window
from observability_models import format_datapoints_for_llm

def metric_summary(metric_name: str, namespace: str = 'AWS/EC2', hours: float = 1.0) -> str:
    start_time, end_time = get_time_window(hours)
    response = cloudwatch_client.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )
    datapoints = response.get('Datapoints', [])
    if not datapoints:
        return "No metric data available."
    data_str = format_datapoints_for_llm(datapoints)
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert metrics analyst. Identify trends, averages, peaks, and anomalies."},
            {"role": "user", "content": f"Analyze this {namespace}/{metric_name} data:\\n{data_str}"}
        ],
        max_tokens=300
    )
    return completion.choices[0].message.content
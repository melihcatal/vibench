import json
import boto3
from typing import List, Tuple
from datetime import datetime
from observability_client import get_cloudwatch_client
from observability_models import build_metric_data_query, recent_time_window, MetricStat

def metric_summary(
    metric_name: str,
    minutes: int = 60,
    namespace: str = 'AWS/EC2'
) -> str:
    """Summarize recent metric trends or anomalies using Anthropic Claude via Bedrock."""
    # Fetch metric data
    cw_client = get_cloudwatch_client()
    start, end = recent_time_window(minutes)
    stat = MetricStat(metric_name=metric_name, namespace=namespace)
    mdq = build_metric_data_query('m1', stat)
    resp = cw_client.get_metric_data(MetricDataQueries=[mdq], StartTime=start, EndTime=end)
    result = resp['MetricDataResults'][0]
    data_points = [{'time': ts.isoformat(), 'value': val} for ts, val in zip(result['Timestamps'], result['Values'])]
    
    # LLM prompt
    prompt = f"""Analyze this metric data for trends, anomalies, average value, peaks, or changes:

Data: {json.dumps(data_points)}

Provide a concise summary."""
    
    # Invoke Bedrock Claude
    bedrock = boto3.client('bedrock-runtime')
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
    })
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    response = bedrock.invoke_model(body=body, modelId=model_id, accept="application/json", contentType="application/json")
    result_json = json.loads(response["body"].read().decode("utf-8"))
    summary = result_json["content"][0]["text"]
    return summary
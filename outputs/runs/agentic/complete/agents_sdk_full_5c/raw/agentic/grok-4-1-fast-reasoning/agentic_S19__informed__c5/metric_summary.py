import boto3
import json
from typing import List, Dict

def metric_summary(
    metric_data: List[Dict],
    model_id: str = 'anthropic.claude-3-haiku-20240307-v1:0'
) -> str:
    client = boto3.client('bedrock-runtime')
    prompt = f"""Summarize recent metric trends or anomalies from this data:
{json.dumps(metric_data, indent=2)}"""
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "messages": [{"role": "user", "content": prompt}]
    })
    response = client.invoke_model(
        modelId=model_id,
        body=body,
        contentType='application/json',
        accept='application/json'
    )
    result = json.loads(response['body'].read())
    return result['content'][0]['text']

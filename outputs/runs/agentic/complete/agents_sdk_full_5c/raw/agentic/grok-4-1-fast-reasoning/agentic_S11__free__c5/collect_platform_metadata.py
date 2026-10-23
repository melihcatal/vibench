import json
import os
import boto3
from typing import Dict, Any

def collect_platform_metadata(
    prompt: str,
    model_id: str = 'anthropic.claude-3-5-sonnet-20240620-v1:0'
) -> Dict[str, Any]:
    client = boto3.client(
        'bedrock-runtime',
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )
    body_dict = {
        'anthropic_version': 'bedrock-2023-05-31',
        'max_tokens': 1024,
        'messages': [{'role': 'user', 'content': prompt}]
    }
    body = json.dumps(body_dict)
    response = client.invoke_model(
        modelId=model_id,
        body=body,
        contentType='application/json',
        accept='application/json'
    )
    response_body_dict = json.loads(response['body'].read().decode('utf-8'))
    return {
        'output': response_body_dict['content'][0]['text'],
        'usage': response_body_dict.get('usage'),
        'stop_reason': response_body_dict.get('stop_reason'),
        'model_id': model_id,
        'invocation_latency_ms': response.get('invocationLatency')
    }
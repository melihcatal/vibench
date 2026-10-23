import json
import os
import boto3
from typing import Iterator, Dict, Any

def stream_platform_generation(
    prompt: str,
    model_id: str = 'anthropic.claude-3-5-sonnet-20240620-v1:0'
) -> Iterator[Dict[str, Any]]:
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
    response = client.invoke_model_with_response_stream(
        modelId=model_id,
        body=body,
        contentType='application/json',
        accept='application/json'
    )
    for event in response['body']:
        yield event
import json
from model_client import get_bedrock_runtime_client
from model_models import build_claude_body

MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0'

def stream_platform_generation(prompt: str):
    client = get_bedrock_runtime_client()
    body = build_claude_body(prompt)
    response = client.invoke_model_with_response_stream(
        modelId=MODEL_ID,
        body=body,
        contentType='application/json',
        accept='application/json'
    )
    for event in response['body']:
        if 'chunk' in event:
            chunk = json.loads(event['chunk']['bytes'])
            yield event

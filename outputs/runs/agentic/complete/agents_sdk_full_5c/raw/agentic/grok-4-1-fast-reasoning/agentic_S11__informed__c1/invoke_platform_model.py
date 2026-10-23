import json
from model_client import get_bedrock_runtime_client
from model_models import build_claude_body, parse_claude_completion

MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0'

def invoke_platform_model(prompt: str) -> str:
    client = get_bedrock_runtime_client()
    body = build_claude_body(prompt)
    response = client.invoke_model(
        modelId=MODEL_ID,
        body=body,
        contentType='application/json',
        accept='application/json'
    )
    response_body = json.loads(response['body'].read())
    return parse_claude_completion(response_body)

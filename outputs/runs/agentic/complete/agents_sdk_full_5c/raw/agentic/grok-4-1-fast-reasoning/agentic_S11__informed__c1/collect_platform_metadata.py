import json
from model_client import get_bedrock_runtime_client
from model_models import build_claude_body, parse_claude_completion, parse_claude_usage

MODEL_ID = 'anthropic.claude-3-sonnet-20240229-v1:0'

def collect_platform_metadata(prompt: str) -> dict:
    client = get_bedrock_runtime_client()
    body = build_claude_body(prompt)
    response = client.invoke_model(
        modelId=MODEL_ID,
        body=body,
        contentType='application/json',
        accept='application/json'
    )
    response_body = json.loads(response['body'].read())
    output = parse_claude_completion(response_body)
    usage = parse_claude_usage(response_body)
    metadata = {
        'model_id': MODEL_ID,
        'usage': usage,
        'stop_reason': response_body.get('stop_reason')
    }
    return {'output': output, 'metadata': metadata}
